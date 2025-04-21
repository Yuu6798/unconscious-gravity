import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from unconscious_gravity_exp.proxy_config import TurnLog

PROJECT_ROOT = Path(__file__).parent.parent

def test_dummy_dialog_creates_parquet(tmp_path, monkeypatch):
    # プロジェクトルートに移動
    monkeypatch.chdir(PROJECT_ROOT)

    # 既存の出力をクリア
    out_dir = PROJECT_ROOT / "data"
    if out_dir.exists():
        for p in out_dir.iterdir():
            p.unlink()
    else:
        out_dir.mkdir()

    # dummy_dialog.py を実行
    result = subprocess.run(
        [sys.executable, "examples/dummy_dialog.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"dummy_dialog.py 実行失敗:\n{result.stderr}"

    # Parquet ファイルの存在を確認
    parquet_path = out_dir / "sample_dialog.parquet"
    assert parquet_path.exists(), "sample_dialog.parquet が作成されていません"

    # データを読み込み、行数とスキーマをチェック
    df = pd.read_parquet(parquet_path)
    assert len(df) == 10, f"行数が10ではありません: {len(df)}"

    expected_cols = list(TurnLog.__annotations__.keys())
    assert set(df.columns) == set(expected_cols), f"スキーマが一致しません: {df.columns.tolist()}"
