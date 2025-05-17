# por_log_writer.py — PoR照合結果ログ保存スクリプト（改良版）

import json
import os
from datetime import datetime
from typing import List, Tuple, Dict, Optional
import logging
from por_inference import PoRInference  # 実行例のため残す

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PoRLogWriter:
    """PoR照合結果をログに保存するクラス"""

    def __init__(self, log_path: str = "por_log.jsonl", max_file_size_mb: int = 10, buffer_size_limit: int = 100):
        """
        初期化

        Args:
            log_path (str): ログファイルのパス（デフォルト: por_log.jsonl）
            max_file_size_mb (int): ログファイルの最大サイズ（MB）
            buffer_size_limit (int): ログエントリのバッファサイズ制限
        """
        self.log_path = log_path
        self.max_file_size_mb = max_file_size_mb
        self.buffer: List[Dict] = []  # ログエントリのバッファ
        self.buffer_size_limit = buffer_size_limit
        self._ensure_log_directory_exists()

    def _ensure_log_directory_exists(self) -> None:
        """ログファイルのディレクトリが存在しない場合は作成する"""
        os.makedirs(os.path.dirname(self.log_path) or '.', exist_ok=True)

    def _rotate_log_file(self) -> None:
        """ログファイルが最大サイズを超えた場合、ローテーション"""
        try:
            if os.path.exists(self.log_path) and os.path.getsize(self.log_path) / (1024 * 1024) > self.max_file_size_mb:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_path = f"{self.log_path}.{timestamp}"
                os.rename(self.log_path, new_path)
                logger.info(f"Rotated log file to {new_path}")
        except FileNotFoundError:
            logger.warning(f"Log file not found at {self.log_path}, no rotation needed.")
        except (OSError, PermissionError) as e:
            logger.error(f"Failed to rotate log file: {e}")

    def _validate_entry(self, entry: Dict) -> bool:
        """ログエントリの必須フィールドを検証"""
        required_fields = ["question", "score", "timestamp", "context", "time_score", "threshold", "fired"]
        return all(field in entry for field in required_fields)

    def log_results(self, results: List[Tuple[str, float]], context: str, time_score: float, threshold: float, extra_data: Optional[Dict] = None) -> None:
        """
        PoR照合結果をJSONL形式でログに保存

        Args:
            results (List[Tuple[str, float]]): 質問とPoRスコアのリスト
            context (str): 照合コンテキスト
            time_score (float): 時系列的照合スコア
            threshold (float): PoRスコアの閾値
            extra_data (Optional[Dict]): ログエントリに追加する任意のデータ
        """
        try:
            for question, score in results:
                entry = {
                    "question": question,
                    "score": score,
                    "timestamp": datetime.now().isoformat(),
                    "context": context,
                    "time_score": time_score,
                    "threshold": threshold,
                    "fired": score >= threshold,
                }
                if extra_data:
                    entry.update(extra_data)

                if self._validate_entry(entry):
                    self.buffer.append(entry)
                else:
                    logger.warning(f"Invalid log entry: {entry}")

            if len(self.buffer) >= self.buffer_size_limit:
                self._flush_buffer()

        except Exception as e:
            logger.error(f"Error logging results: {e}")

    def flush(self) -> None:
        """バッファの内容を強制的にログファイルに書き込む"""
        self._flush_buffer()

    def _flush_buffer(self) -> None:
        """バッファの内容をログファイルに書き込み"""
        if not self.buffer:
            return

        try:
            self._rotate_log_file()
            with open(self.log_path, "a", encoding="utf-8") as f:
                for entry in self.buffer:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            logger.info(f"Wrote {len(self.buffer)} entries to {self.log_path}")
            self.buffer.clear()
        except (OSError, PermissionError) as e:
            logger.error(f"Failed to write log: {e}")

    def __del__(self):
        """デストラクタでバッファをフラッシュ"""
        self._flush_buffer()

# 実行例
if __name__ == "__main__":
    por = PoRInference(threshold=0.5)
    log_writer = PoRLogWriter(log_path="logs/por_log.jsonl", max_file_size_mb=5, buffer_size_limit=50)

    questions = [
        "What is consciousness?",
        "What is 2 + 2?",
        "Can machines feel regret?",
        "Define entropy.",
        "Explain the weather tomorrow."
    ]
    context = "This is a conversation about AI and consciousness in philosophical context."
    time_score = 0.9

    results = por.select_by_por(questions, context, time_score)
    log_writer.log_results(results, context, time_score, por.threshold, extra_data={"model_version": "v1.0"})

    # 必要に応じて明示的にフラッシュすることも可能
    # log_writer.flush()

    print("Logged the following PoR-fired entries:")
    for question, score in results:
        print(f"- {question} [E = {score:.4f}]")
