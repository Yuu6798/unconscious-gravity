#!/usr/bin/env python3
"""Generate a sample 10-turn dialog and store it as parquet."""

import argparse
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from unconscious_gravity_exp.logger import append_log  # noqa: E402
from unconscious_gravity_exp.proxy_config import TurnLog  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=PROJECT_ROOT / "data" / "sample_dialog.parquet",
        help="Output parquet file path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_file = args.out
    out_file.parent.mkdir(parents=True, exist_ok=True)

    for i in range(1, 11):
        turn = TurnLog(
            TurnId=i,
            Prompt=f"User prompt {i}",
            Response=f"AI response {i}",
            Q_self=random.random(),
            S_q=random.random(),
            t_total=random.randint(50, 500),
            M=random.random(),
        )
        append_log(turn, file=str(out_file))
        print(f"[{i}] wrote: {out_file}")


if __name__ == "__main__":
    main()
