import subprocess
import sys
from pathlib import Path

import pandas as pd

from unconscious_gravity_exp.proxy_config import TurnLog

PROJECT_ROOT = Path(__file__).parent.parent


def test_dummy_dialog_creates_parquet(tmp_path):
    parquet_path = tmp_path / "sample_dialog.parquet"

    result = subprocess.run(
        [sys.executable, "examples/dummy_dialog.py", "--out", str(parquet_path)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"dummy_dialog.py failed:\n{result.stderr}"
    assert parquet_path.exists(), "sample_dialog.parquet was not created"

    df = pd.read_parquet(parquet_path)
    assert len(df) == 10, f"Expected 10 rows, got {len(df)}"

    expected_cols = list(TurnLog.__annotations__.keys())
    assert set(df.columns) == set(expected_cols), f"Unexpected schema: {df.columns.tolist()}"
