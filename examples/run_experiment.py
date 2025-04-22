import argparse
from pathlib import Path
from unconscious_gravity_exp.inference import infer
from unconscious_gravity_exp.proxy_config import TurnLog
from unconscious_gravity_exp.logger import append_log

def main():
    parser = argparse.ArgumentParser(description="Run multi-episode UGHER inference experiment")
    parser.add_argument("--episodes", type=int, default=1, help="Number of episodes to simulate")
    parser.add_argument("--turns", type=int, default=5, help="Number of turns per episode")
    parser.add_argument("--log", type=str, default="data/sample.parquet", help="Output log file")
    parser.add_argument("--out_dir", type=str, default="data", help="Output directory")
    args = parser.parse_args()

    Path(args.out_dir).mkdir(exist_ok=True)

    turn_id = 1
    for ep in range(1, args.episodes + 1):
        print(f"[Episode {ep}]")
        for t in range(1, args.turns + 1):
            prompt = f"What is PoR in context {ep}.{t}?"
            response = infer(prompt)
            turn = TurnLog(
                TurnId=turn_id,
                Prompt=prompt,
                Response=response,
                Q_self=0.7,
                S_q=0.9,
                t_total=150,
                M=0.5
            )
            append_log(turn, file=args.log)
            print(f"Logged Turn {turn_id}: {prompt} -> {response}")
            turn_id += 1

if __name__ == "__main__":
    main()