# por_diagnostics/diagnostic.py
"""
PoR Log Diagnostic System

Provides utilities to parse PoR logs, evaluate quality metrics, and generate markdown reports.
"""
import json
from pathlib import Path
from typing import List, Dict, Any


class PoRDiagnostic:
    """
    Parses JSON-formatted PoR log entries, computes quality metrics, and generates a markdown report.
    """
    def __init__(self, log_dir: Path):
        """
        :param log_dir: Directory containing PoR log files (each a JSON object per file).
        """
        self.log_dir = log_dir
        self.logs: List[Dict[str, Any]] = []

    def load_logs(self) -> None:
        """
        Load all JSON log files from the log directory into memory.
        """
        self.logs.clear()
        for filepath in self.log_dir.glob("*.json"):
            try:
                with filepath.open('r', encoding='utf-8') as f:
                    entry = json.load(f)
                self.logs.append(entry)
            except json.JSONDecodeError as e:
                # Skip invalid JSON and continue
                print(f"Warning: could not parse {filepath}: {e}")

    def analyze_logs(self) -> Dict[str, Any]:
        """
        Analyze loaded logs and compute quality metrics.

        Returns:
            A dict containing metrics such as total_entries, error_count,
            average_latency_ms, success_rate.
        """
        metrics: Dict[str, Any] = {
            'total_entries': len(self.logs),
            'error_count': 0,
            'latencies': [],  # intermediate list
        }

        for entry in self.logs:
            status = entry.get('status')
            if status != 'ok':
                metrics['error_count'] += 1
            if 'latency_ms' in entry:
                metrics['latencies'].append(entry['latency_ms'])

        latencies = metrics.pop('latencies')
        if latencies:
            metrics['average_latency_ms'] = sum(latencies) / len(latencies)
        else:
            metrics['average_latency_ms'] = None

        if metrics['total_entries'] > 0:
            metrics['success_rate'] = (
                (metrics['total_entries'] - metrics['error_count'])
                / metrics['total_entries']
            )
        else:
            metrics['success_rate'] = None

        return metrics

    def generate_report(self, metrics: Dict[str, Any], output_file: Path) -> None:
        """
        Generate a markdown report of diagnostics results.

        :param metrics: Dict of metrics from analyze_logs()
        :param output_file: Path to write the markdown report
        """
        lines: List[str] = [
            '# PoR Diagnostic Report',
            f"- Total entries: {metrics.get('total_entries', 0)}",
            f"- Error count: {metrics.get('error_count', 0)}",
        ]
        avg = metrics.get('average_latency_ms')
        if avg is not None:
            lines.append(f"- Average latency: {avg:.2f} ms")
        else:
            lines.append("- Average latency: N/A")

        success = metrics.get('success_rate')
        if success is not None:
            lines.append(f"- Success rate: {success * 100:.1f}%")
        else:
            lines.append("- Success rate: N/A")

        output_file.write_text("\n".join(lines), encoding='utf-8')

    def run(self, output_dir: Path) -> None:
        """
        Full pipeline: load logs, analyze, and write report to output_dir/por_eval_result.md.
        """
        self.load_logs()
        metrics = self.analyze_logs()
        report_path = output_dir / 'por_eval_result.md'
        self.generate_report(metrics, report_path)