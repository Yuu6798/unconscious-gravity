import os
import time
from pathlib import Path

import pandas as pd

from .proxy_config import TurnLog

# デフォルトのログファイル名と最大サイズ (50MB)
LOG_FILE = "por_logs.parquet"
MAX_FILE_SIZE = 50 * 1024 * 1024  # bytes


def append_log(turn: TurnLog, file: str = LOG_FILE) -> None:
    """指定された ``file`` に ``TurnLog`` を追記保存する。

    ログファイルのサイズが ``MAX_FILE_SIZE`` を超えるときは自動で
    同じディレクトリ内にタイムスタンプ付きの名前でローテーションする。
    """
    path = Path(file)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > MAX_FILE_SIZE:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        rotated_name = path.with_name(f"{path.stem}_{timestamp}{path.suffix}")
        path.rename(rotated_name)

    # TurnLog を DataFrame に変換
    df_new = pd.DataFrame([turn.__dict__])

    if os.path.exists(file):
        # 既存ログを読み込んで新規行を連結
        df_existing = pd.read_parquet(file)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        # ログファイルがなければ新規作成
        df_all = df_new

    # Parquet に書き戻す
    df_all.to_parquet(file, engine="pyarrow", index=False)
