import pytest

from ugh3_metrics import calc_por, calc_delta_e, calc_grv


@pytest.mark.parametrize("q,s_q,t,expected", [
    (1.0, 1.2, 0.8, 0.96),
    (2.0, 0.5, 1.0, 1.0),
])
def test_calc_por(q, s_q, t, expected):
    assert calc_por(q, s_q, t) == pytest.approx(expected)

def test_calc_por_invalid():
    with pytest.raises(TypeError):
        calc_por("a", 1.0, 0.5)


@pytest.mark.parametrize("curr,prev,expected", [
    (3.0, 2.5, 0.5),
    (1.0, 3.0, 2.0),
])
def test_calc_delta_e(curr, prev, expected):
    assert calc_delta_e(curr, prev) == pytest.approx(expected)

def test_calc_delta_e_invalid():
    with pytest.raises(TypeError):
        calc_delta_e(1.0, None)


@pytest.mark.parametrize("freq,entropy,expected", [
    (2.0, 0.5, 1.0),
    (0.0, 1.0, 0.0),
])
def test_calc_grv(freq, entropy, expected):
    assert calc_grv(freq, entropy) == pytest.approx(expected)

def test_calc_grv_invalid():
    with pytest.raises(TypeError):
        calc_grv(1.0, "x")
