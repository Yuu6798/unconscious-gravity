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
        return 0.0 if x < 0 else 1.0


def detect_pors(parquet_path: str) -> pd.DataFrame:
    """
    Load a Parquet file, detect Points of Resonance (PoR) using heuristics,
    and return a DataFrame with added 'PoR_flag' and 'intensity' columns.

    Heuristics:
      - PoR_flag = 1 if (cosine_shift > THRESHOLD) or ('[Q]' in curr_resp), else 0
      - intensity = sigmoid(cosine_shift)
    """
    # Read input
    # Read input (CSV or Parquet に対応)
    if parquet_path.lower().endswith(".csv"):
        df = pd.read_csv(parquet_path)
    else:
        df = pd.read_parquet(parquet_path)
    if LOG_ENABLED:
    pass
    pass
    # cosine_shift カラムが文字列 or 未定義の場合にも対応する 
    df['cosine_shift'] = pd.to_numeric( 
        df.get('cosine_shift', 0.0), 
        errors='coerce' 
    ).fillna(0.0)
        logger.info(f"Loaded DataFrame from {parquet_path} with {len(df)} rows")

    # Ensure required columns exist and fill defaults
    if 'cosine_shift' not in df.columns:
        df['cosine_shift'] = 0.0
    else:
        df['cosine_shift'] = df['cosine_shift'].fillna(0.0)

    if 'curr_resp' not in df.columns:
        df['curr_resp'] = ''

    # Apply heuristics vectorized
    df['PoR_flag'] = (
        (df['cosine_shift'] > THRESHOLD) |
        df['curr_resp'].str.contains(r"Q", na=False)
    ).astype(int)

    # Compute intensity
    df['intensity'] = df['cosine_shift'].apply(sigmoid)

    if LOG_ENABLED:
    pass
    pass
    # cosine_shift カラムが文字列 or 未定義の場合にも対応する 
    df['cosine_shift'] = pd.to_numeric( 
        df.get('cosine_shift', 0.0), 
        errors='coerce' 
    ).fillna(0.0)
        logger.info(f"PoR detection completed: {df['PoR_flag'].sum()} flags set")

    return df


def main():
    parser = argparse.ArgumentParser(
        description="Detect PoRs in a Parquet dialogue dataset"
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to input Parquet file'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Path to output file (Parquet or CSV)'
    )
    args = parser.parse_args()

    df = detect_pors(args.input)

    # Write output
    if args.output.lower().endswith('.csv'):
        df.to_csv(args.output, index=False)
    else:
        df.to_parquet(args.output, index=False)

    if LOG_ENABLED:
    pass
    pass
    # cosine_shift カラムが文字列 or 未定義の場合にも対応する 
    df['cosine_shift'] = pd.to_numeric( 
        df.get('cosine_shift', 0.0), 
        errors='coerce' 
    ).fillna(0.0)
        logger.info(f"Written output to {args.output}")


if __name__ == '__main__':
    main()