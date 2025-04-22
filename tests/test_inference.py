import subprocess
import sys
from pathlib import Path
import pandas as pd
import pytest

from unconscious_gravity_exp.inference import infer

def test_infer_echo():
    prompt = "What is PoR?"
    response = infer(prompt)
    assert "[ECHOED]" in response
    assert prompt in response

def test_run_experiment_generates_parquet(tmp_path):
    out_dir = tmp_path / "data"
    out_dir.mkdir()
    log_file = out_dir / "experiment.parquet"

    result = subprocess.run([
        sys.executable, "examples/run_experiment.py",
        "--episodes", "2",
        "--turns", "3",
        "--out_dir", str(out_dir),
        "--log", str(log_file)
    ], capture_output=True, text=True)

    assert result.returncode == 0, f"run_experiment.py failed:\n{result.stderr}"
    assert log_file.exists(), "Expected Parquet log file not found"

    df = pd.read_parquet(log_file)
    assert len(df) == 6, f"Expected 6 rows, got {len(df)}"
    assert "Prompt" in df.columns
    assert "Response" in df.columns