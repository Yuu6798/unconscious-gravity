# src/por_diagnostics/cli.py
import argparse
from pathlib import Path
from .diagnostic import PoRDiagnostic

def main():
    parser = argparse.ArgumentParser(
        description="Run PoR log diagnostics"
    )
    parser.add_argument(
        "-l", "--log-dir", type=Path, required=True,
        help="Directory containing PoR JSON logs"
    )
    parser.add_argument(
        "-o", "--out-dir", type=Path, required=True,
        help="Directory to write the markdown report"
    )
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    PoRDiagnostic(args.log_dir).run(args.out_dir)

if __name__ == "__main__":
    main()
