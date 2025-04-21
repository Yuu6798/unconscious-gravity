import json
import pytest
from pathlib import Path
from por_diagnostics.diagnostic import PoRDiagnostic

@pytest.fixture
def sample_logs(tmp_path):
    # Create sample JSON log files
    log1 = tmp_path / "log1.json"
    log1.write_text(json.dumps({"status": "ok", "latency_ms": 50}))
    log2 = tmp_path / "log2.json"
    log2.write_text(json.dumps({"status": "error", "latency_ms": 150}))
    log3 = tmp_path / "invalid.json"
    log3.write_text("not a json")
    return tmp_path

def test_load_and_analyze(sample_logs, capsys):
    diag = PoRDiagnostic(sample_logs)
    diag.load_logs()
    metrics = diag.analyze_logs()
    assert metrics["total_entries"] == 2
    assert metrics["error_count"] == 1
    assert pytest.approx(metrics["average_latency_ms"], 0.1) == (50 + 150) / 2
    assert pytest.approx(metrics["success_rate"], 0.01) == (2 - 1) / 2

def test_generate_report(tmp_path, sample_logs):
    diag = PoRDiagnostic(sample_logs)
    diag.load_logs()
    metrics = diag.analyze_logs()
    report_file = tmp_path / "por_eval_result.md"
    diag.generate_report(metrics, report_file)
    content = report_file.read_text()
    assert "# PoR Diagnostic Report" in content
    assert "- Total entries: 2" in content
    assert "- Error count: 1" in content
    assert "- Average latency: 100.00 ms" in content
    assert "- Success rate: 50.0%" in content