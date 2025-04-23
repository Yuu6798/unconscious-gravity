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

    # Ensure required columns exist and fill defaults, converting types as needed
    if 'cosine_shift' not in df.columns:
        df['cosine_shift'] = 0.0
    else:
        # fill missing and coerce to float
        df['cosine_shift'] = pd.to_numeric(df['cosine_shift'], errors='coerce') \
                               .fillna(0.0)

    if 'curr_resp' not in df.columns:
        df['curr_resp'] = ''
    else:
        # ensure it's string type
        df['curr_resp'] = df['curr_resp'].astype(str)

    # Apply heuristics vectorized
    df['PoR_flag'] = (
        (df['cosine_shift'] > THRESHOLD) |
        df['curr_resp'].str.contains(r"Q", na=False)
    ).astype(int)

    # Compute intensity
    df['intensity'] = df['cosine_shift'].apply(sigmoid)

    if LOG_ENABLED:
        logger.info(f"PoR detection completed: {df['PoR_flag'].sum()} flags set")

    return df

def main():
    parser = argparse.ArgumentParser(
        description="Detect PoRs in a Parquet or CSV dialogue dataset"
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to input Parquet or CSV file'
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
        logger.info(f"Written output to {args.output}")

if __name__ == '__main__':
    main()