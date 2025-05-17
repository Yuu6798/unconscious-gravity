import pandas as pd
from pandas.testing import assert_series_equal

from ugher_exp.por_detector import detect_pors, THRESHOLD, sigmoid

MARKER = "\ue001Q\ue001"

def make_df():
    return pd.DataFrame(
        {
            "cosine_shift": [0.5, 0.1, 0.2],
            "curr_resp": ["hi", f"hello {MARKER}", "nothing"]
        }
    )


def expected_flags(df):
    return pd.Series([int(df.loc[i, "cosine_shift"] > THRESHOLD or MARKER in df.loc[i, "curr_resp"]) for i in df.index])


def expected_intensity(df):
    return df["cosine_shift"].apply(sigmoid)


def test_detect_pors_csv(tmp_path):
    df = make_df()
    path = tmp_path / "sample.csv"
    df.to_csv(path, index=False)

    result = detect_pors(str(path))

    assert "PoR_flag" in result.columns
    assert "intensity" in result.columns
    assert_series_equal(result["PoR_flag"], expected_flags(df), check_names=False)
    assert_series_equal(result["intensity"], expected_intensity(df), check_names=False)


def test_detect_pors_parquet(tmp_path):
    df = make_df()
    path = tmp_path / "sample.parquet"
    df.to_parquet(path)

    result = detect_pors(str(path))

    assert_series_equal(result["PoR_flag"], expected_flags(df), check_names=False)
    assert_series_equal(result["intensity"], expected_intensity(df), check_names=False)
