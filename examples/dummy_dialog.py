#!/usr/bin/env python3
"""
10件のダミー対話ターンを生成し、
logger.append_log で Parquet ファイルに書き出すスモークテスト用スクリプト
"""

import sys
from pathlib import Path
import random

# プロジェクトの src フォルダをインポートパスに追加
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / "src"))

from unconscious_gravity_exp.proxy_config import TurnLog
from unconscious_gravity_exp.logger import append_log

def main():
    # 出力先ディレクトリとファイル名
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    out_file = data_dir / "sample_dialog.parquet"

    # 10件のダミーデータを逐次書き込み
    for i in range(1, 11):
        turn = TurnLog(
            TurnId=i,
            Prompt=f"ユーザーの発話 {i}",
            Response=f"AIの応答 {i}",
            Q_self=random.random(),
            S_q=random.random(),
            t_total=random.randint(50, 500),  # ミリ秒
            M=random.random()
        )
        append_log(turn, file=str(out_file))
        print(f"[{i}] 書き込み完了 → {out_file}")

if __name__ == "__main__":
    main()