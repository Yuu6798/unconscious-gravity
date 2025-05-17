import pandas as pd
import pytest

from ugher_exp.por_detector import detect_pors
from models.por_formal_models import PoRModel


def test_por_detection_fail(tmp_path):
    df = pd.DataFrame({"cosine_shift": [0.1], "curr_resp": ["hello"]})
    path = tmp_path / "input.parquet"
    df.to_parquet(path)
    result = detect_pors(str(path))
    assert result["PoR_flag"].sum() == 0


def test_low_grv_score():
    grv = PoRModel.semantic_gravity(0.1, 0.05)
    assert grv < 0.01

