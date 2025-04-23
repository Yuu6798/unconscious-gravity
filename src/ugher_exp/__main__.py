import argparse
from pathlib import Path
from unconscious_gravity_exp.proxy_config import TurnLog
from unconscious_gravity_exp.logger import append_log

def main():
    parser = argparse.ArgumentParser(description="UGHer CLI runner")
    parser.add_argument("--log", type=str, default="data/sample.parquet", help="Output Parquet file")
    parser.add_argument("--turns", type=int, default=5, help="Number of dummy turns to simulate")
    args = parser.parse_args()

    Path("data").mkdir(exist_ok=True)

    for i in range(1, args.turns + 1):
        turn = TurnLog(
            TurnId=i,
            Prompt=f"Prompt {i}",
            Response=f"Response {i}",
            Q_self=0.5,
            S_q=0.8,
            t_total=100 + i,
            M=0.2 * i
        )
        append_log(turn, file=args.log)
        print(f"[{i}] TurnLog written to {args.log}")

if __name__ == "__main__":
    main()