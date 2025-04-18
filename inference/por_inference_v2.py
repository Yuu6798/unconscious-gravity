# inference/por_inference_v2.py

import numpy as np
from typing import Optional, List, Tuple
from sentence_transformers import SentenceTransformer
from models.por_formal_models import PoRModel
import logging

# ログ設定（改善点5：ログ機能の追加）
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PoRInference:
    """
    Interface for semantic inference of PoR (Point of Resonance).
    Estimates semantic density S_q via embeddings and computes existence E.
    """
    def __init__(
        self,
        model: PoRModel = PoRModel,
        embed_model_name: str = 'all-MiniLM-L6-v2'
    ):
        """
        Initialize PoR inference with embedding model and PoRModel.

        Args:
            model: PoRModel class or instance.
            embed_model_name: Name of SentenceTransformer model.
        """
        self.model = model
        try:
            # 改善点6：モデルのカスタマイズ性向上
            self.embedder = SentenceTransformer(embed_model_name)
            logger.info(f"Loaded embedding model: {embed_model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model {embed_model_name}: {e}")
            raise ValueError(f"Invalid embed_model_name: {e}")

    def compute_semantic_density(self, question: str) -> float:
        """
        Compute semantic density S_q as the norm of the embedding vector with normalization.

        Args:
            question: Input question string.

        Returns:
            Semantic density (float).
        """
        # 改善点1：エラー処理の追加
        if not question or not isinstance(question, str):
            logger.error("Invalid input: question must be a non-empty string")
            raise ValueError("question must be a non-empty string")

        try:
            emb = self.embedder.encode(question, convert_to_numpy=True)
            norm = float(np.linalg.norm(emb))
            # 改善点2：セマンティック密度の正規化（例：0～1の範囲にスケーリング）
            # 仮にノルムの最大値を仮定（SentenceTransformerの出力ノルムはモデル依存）
            max_norm = 10.0  # モデルに応じて調整可能
            S_q = norm / max_norm
            logger.debug(f"Computed S_q for '{question}': {S_q}")
            return min(max(S_q, 0.0), 1.0)  # 0～1にクリップ
        except Exception as e:
            logger.error(f"Error computing semantic density for '{question}': {e}")
            raise

    def compute_question_pressure(self, question: str) -> float:
        """
        Estimate question pressure Q based on token length and complexity.

        Args:
            question: Input question string.

        Returns:
            Question pressure factor (float).
        """
        # 改善点1：エラー処理
        if not question or not isinstance(question, str):
            logger.error("Invalid input: question must be a non-empty string")
            raise ValueError("question must be a non-empty string")

        # 改善点3：質問圧力の計算ロジック改善（トークン長＋構文複雑さを考慮）
        tokens = question.split()
        length = len(tokens)
        # 構文複雑さ（例：句読点の数や固有名詞の割合を考慮）
        complexity = 1.0 + (question.count("?") + question.count(",")) * 0.1
        max_len = 50
        Q = min(length / max_len * complexity, 1.0)
        logger.debug(f"Computed Q for '{question}': {Q}")
        return Q

    def infer_existence(
        self,
        question: str,
        t: float = 1.0
    ) -> float:
        """
        Infer the existence score E = Q × S_q × t

        Args:
            question: Input question string.
            t: Critical time factor.

        Returns:
            Existence score E (float).
        """
        Q = self.compute_question_pressure(question)
        S_q = self.compute_semantic_density(question)
        E = self.model.existence(Q, S_q, t)
        logger.info(f"Inferred E for '{question}' (t={t}): {E}")
        return E

    def is_resonance(
        self,
        question: str,
        t: float = 1.0,
        threshold: Optional[float] = None
    ) -> bool:
        """
        Determine if PoR fires with dynamic thresholding.

        Args:
            question: Input question string.
            t: Critical time factor.
            threshold: Existence threshold for resonance (if None, dynamically computed).

        Returns:
            True if E > threshold, else False.
        """
        E = self.infer_existence(question, t)
        # 改善点4：動的閾値の計算（例：S_qやQに応じて調整）
        if threshold is None:
            threshold = 0.3 + (self.compute_semantic_density(question) * 0.2)  # 例：S_qに応じて調整
        result = E > threshold
        logger.info(f"Resonance check for '{question}' (E={E}, threshold={threshold}): {result}")
        return result

    # 改善点7：バッチ処理のサポート
    def batch_infer_existence(
        self,
        questions: List[str],
        t: float = 1.0
    ) -> List[float]:
        """
        Infer existence scores for a batch of questions.

        Args:
            questions: List of input question strings.
            t: Critical time factor.

        Returns:
            List of existence scores.
        """
        scores = []
        for question in questions:
            try:
                E = self.infer_existence(question, t)
                scores.append(E)
            except Exception as e:
                logger.error(f"Error processing question '{question}': {e}")
                scores.append(0.0)  # エラー時は0を返す
        return scores

    def batch_is_resonance(
        self,
        questions: List[str],
        t: float = 1.0,
        threshold: Optional[float] = None
    ) -> List[bool]:
        """
        Determine resonance for a batch of questions.

        Args:
            questions: List of input question strings.
            t: Critical time factor.
            threshold: Existence threshold for resonance.

        Returns:
            List of resonance results (True/False).
        """
        results = []
        for question in questions:
            try:
                result = self.is_resonance(question, t, threshold)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing question '{question}': {e}")
                results.append(False)  # エラー時はFalseを返す
        return results

# Example usage with improvements:
if __name__ == "__main__":
    inf = PoRInference(embed_model_name="all-MiniLM-L6-v2")
    
    # 単一質問の処理
    question = "What is presence?"
    score = inf.infer_existence(question, t=0.9)
    fire = inf.is_resonance(question, t=0.9)
    print(f"Single question - Score: {score}, Resonance: {fire}")

    # バッチ処理の例
    questions = ["What is presence?", "How does gravity work?", "Is AI conscious?"]
    scores = inf.batch_infer_existence(questions, t=0.9)
    resonances = inf.batch_is_resonance(questions, t=0.9)
    for q, s, r in zip(questions, scores, resonances):
        print(f"Batch - Question: {q}, Score: {s}, Resonance: {r}")