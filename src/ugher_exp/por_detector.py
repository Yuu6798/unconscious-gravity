import pandas as pd
import math
import argparse

# Optional: integrate with your project logger
try:
    from .logger import logger
    LOG_ENABLED = True
except ImportError:
    logger = None  # type: ignore
    LOG_ENABLED = False

THRESHOLD = 0.35

def sigmoid(x: float) -> float:
    """
    Compute the sigmoid function: 1 / (1 + exp(-x)).
    """
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0.0

def detect_pors(path: str) -> pd.DataFrame:
    """
    Load a Parquet or CSV file, detect Points of Resonance (PoR) using heuristics,
    and return a DataFrame with added 'PoR_flag' and 'intensity' columns.
    """
    # Read input (CSV or Parquet に対応)
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_parquet(path)

    if LOG_ENABLED:
        logger.info(f"Loaded DataFrame from {path} with {len(df)} rows")

    # cosine_shift カラムがない or 文字列のまま の場合に対応
    # → 存在しなければ 0.0, 文字列なら数値に変換（失敗時は NaN→0.0）
    df['cosine_shift'] = pd.to_numeric(
        df.get('cosine_shift', 0.0),
        errors='coerce'
    ).fillna(0.0)

    # curr_resp がない場合は空文字列に
    df['curr_resp'] = df.get('curr_resp', '').fillna('')

    # PoR フラグと強度計算
    df['PoR_flag'] = (
        (df['cosine_shift'] > THRESHOLD)
        | df['curr_resp'].str.contains(r'Q', na=False)
    ).astype(int)

    df['intensity'] = df['cosine_shift'].apply(sigmoid)

    return df

def main():
    parser = argparse.ArgumentParser(description="Detect PoRs in dialogue data")
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input Parquet or CSV file"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to output Parquet or CSV file"
    )
    args = parser.parse_args()

    df = detect_pors(args.input)

    # 出力先に合わせて Parquet/CSV を自動判定
    if args.output.lower().endswith('.csv'):
        df.to_csv(args.output, index=False)
    else:
        df.to_parquet(args.output, index=False)

    if LOG_ENABLED:
        logger.info(f"Wrote results to {args.output}")

if __name__ == "__main__":
    main()