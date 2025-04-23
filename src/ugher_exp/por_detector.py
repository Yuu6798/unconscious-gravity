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

# Threshold for PoR detection
THRESHOLD = 0.35

def sigmoid(x: float) -> float:
    """
    Compute the sigmoid function: 1 / (1 + exp(-x)).
    """
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0

def detect_pors(path: str) -> pd.DataFrame:
    """
    Load a Parquet or CSV file, detect Points of Resonance (PoR) using heuristics,
    and return a DataFrame with added 'PoR_flag' and 'intensity' columns.
    """
    # 1. Read input (CSV or Parquet に対応)
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_parquet(path)

    if LOG_ENABLED:
        logger.info(f"Loaded DataFrame from {path} with {len(df)} rows")

    # 2. 必要なカラムがなければデフォルトを埋める
    if 'cosine_shift' not in df.columns:
        df['cosine_shift'] = 0.0
    else:
        df['cosine_shift'] = pd.to_numeric(
            df['cosine_shift'], errors='coerce'
        ).fillna(0.0)

    if 'curr_resp' not in df.columns:
        df['curr_resp'] = ''
    else:
        df['curr_resp'] = df['curr_resp'].fillna('')

    # 3. PoR フラグ＆強度計算
    df['PoR_flag'] = (
        (df['cosine_shift'] > THRESHOLD)
        | df['curr_resp'].str.contains(r'Q', na=False)
    ).astype(int)

    df['intensity'] = df['cosine_shift'].apply(sigmoid)

    if LOG_ENABLED:
        logger.info(f"PoR detection completed: {df['PoR_flag'].sum()} flags set")

    return df

def main():
    parser = argparse.ArgumentParser(
        description="Detect PoRs in a Parquet or CSV dataset"
    )
    parser.add_argument(
        '--input', '-i', required=True,
        help="Input CSV or Parquet file path"
    )
    parser.add_argument(
        '--output', '-o', required=True,
        help="Output CSV or Parquet file path"
    )
    args = parser.parse_args()

    df = detect_pors(args.input)

    # 4. Save output in matching format
    if args.output.lower().endswith('.csv'):
        df.to_csv(args.output, index=False)
    else:
        df.to_parquet(args.output, index=False)

if __name__ == '__main__':
    main()