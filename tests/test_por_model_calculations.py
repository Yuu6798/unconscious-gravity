import pytest import numpy as np import math

from models.por_formal_models import PoRModel from metadata.semantic_index import semantic_index  # if needed for tags from typing import List

Assuming PoRModelCalculations logic is in models/por_formal_models.py

and methods have same names as listed in semantic_index.json

class TestPoRModelCalculations: @pytest.mark.parametrize("Q,S_q,t,expected", [ (2.0, 3.0, 4.0, 24.0), (1.5, 1.5, 1.5, 3.375), (0.0, 5.0, 10.0, 0.0) ]) def test_existence(self, Q: float, S_q: float, t: float, expected: float): assert math.isclose(PoRModel.existence(Q, S_q, t), expected, rel_tol=1e-9)

@pytest.mark.parametrize("E_base,delta,Q_self,expected", [
    (10.0, 2.0, 0.5, 11.0),
    (0.0, 5.0, 1.0, 5.0)
])
def test_self_por_score(self, E_base: float, delta: float, Q_self: float, expected: float):
    assert math.isclose(PoRModel.self_por_score(E_base, delta, Q_self), expected, rel_tol=1e-9)

@pytest.mark.parametrize("E,Q,expected", [
    (10.0, 7.0, 3.0),
    (5.5, 5.5, 0.0)
])
def test_mismatch(self, E: float, Q: float, expected: float):
    assert PoRModel.mismatch(E, Q) == expected

@pytest.mark.parametrize("freq,entropy,expected", [
    (2.0, 3.0, 6.0),
    (0.0, 10.0, 0.0)
])
def test_semantic_gravity(self, freq: float, entropy: float, expected: float):
    assert math.isclose(PoRModel.semantic_gravity(freq, entropy), expected, rel_tol=1e-9)

@pytest.mark.parametrize("lam,t,expected", [
    (1.0, 0.0, 1.0),
    (0.5, 2.0, 0.5 * math.exp(-1.0))
])
def test_por_collapse_frequency(self, lam: float, t: float, expected: float):
    assert math.isclose(PoRModel.por_collapse_frequency(t, lam), expected, rel_tol=1e-9)

@pytest.mark.parametrize("I_q,E_m,R_def,theta,expected", [
    (10.0, 5.0, 4.0, 8.0, True),
    (1.0, 1.0, 0.0, 2.0, False)
])
def test_por_firing_probability(self, I_q: float, E_m: float, R_def: float, theta: float, expected: bool):
    assert PoRModel.por_firing_probability(I_q, E_m, R_def, theta) == expected

def test_refire_difference(self):
    assert PoRModel.refire_difference(10.0, 7.5) == 2.5
    with pytest.raises(TypeError):
        PoRModel.refire_difference("a", 1.0)

@pytest.mark.parametrize("ref_flow,d_in,d_out,expected", [
    (100.0, 5.0, 5.0, 100.0/10.0)
])
def test_self_coherence(self, ref_flow: float, d_in: float, d_out: float, expected: float):
    assert math.isclose(PoRModel.self_coherence(ref_flow, d_in, d_out), expected, rel_tol=1e-9)
    with pytest.raises(ZeroDivisionError):
        PoRModel.self_coherence(1.0, 0.0, 0.0)

def test_gravity_tensor(self):
    res = PoRModel.gravity_tensor([1, 2], [0.5, 0.5])
    assert math.isclose(res, 1*0.5 + 2*0.5, rel_tol=1e-9)

@pytest.mark.parametrize("k,E,S,gamma,expected", [
    (1.0, 2.0, 3.0, 2.0, 1.0*2.0*3.0**2.0)
])
def test_phase_gradient(self, k: float, E: float, S: float, gamma: float, expected: float):
    assert math.isclose(PoRModel.phase_gradient(E, S, k, gamma), expected, rel_tol=1e-9)
    with pytest.raises(ValueError):
        PoRModel.phase_gradient(1.0, -1.0, 1.0, 0.5)

