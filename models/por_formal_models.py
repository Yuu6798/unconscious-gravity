# models/por_formal_models.py

import math
from typing import List, Optional

class PoRModel: """Core PoR (Point of Resonance) model calculations."""

@staticmethod
def existence(Q: float, S_q: float, t: float) -> float:
    """E = Q × S_q × t"""
    return Q * S_q * t

@staticmethod
def self_por_score(
    E_base: float,
    delta_E_over: float,
    Q_self_factor: float
) -> float:
    """E_self = E_base + ΔE_over × Q_self_factor"""
    return E_base + delta_E_over * Q_self_factor

@staticmethod
def mismatch(E: float, Q: float) -> float:
    """Mismatch = |E - Q|"""
    return abs(E - Q)

@staticmethod
def semantic_gravity(por_freq: float, entropy: float) -> float:
    """Semantic gravity = por_freq × entropy"""
    return por_freq * entropy

@staticmethod
def por_collapse_frequency(lam: float, t: float) -> float:
    """λ·e^(−λt)"""
    return lam * math.exp(-lam * t)

@staticmethod
def refire_difference(I_q: float, R_def: float) -> float:
    """Difference = I_q - R_def"""
    return I_q - R_def

@staticmethod
def self_coherence(
    ref_flow: float,
    d_in: float,
    d_out: float
) -> float:
    """ref_flow / (d_in + d_out)"""
    return ref_flow / (d_in + d_out)

@staticmethod
def gravity_tensor(
    flow: List[float],
    weights: List[float]
) -> float:
    """Sum of flow_i * weights_i"""
    return sum(f * w for f, w in zip(flow, weights))

@staticmethod
def phase_gradient(
    E: float,
    S: float,
    k: Optional[float] = None,
    gamma: Optional[float] = None
) -> float:
    """
    位相勾配。
    2 引数版: E × S,
    4 引数版: k × E × S^γ
    """
    # エントロピー S が負ならエラー
    if S < 0:
        raise ValueError("entropy must be non-negative")

    # 2 引数版
    if k is None and gamma is None:
        return E * S

    # k のみ指定
    if k is not None and gamma is None:
        return k * S

    # k, gamma 両方指定
    return k * E * (S ** gamma)

@staticmethod
def is_por_null(
    output: str,
    keywords: List[str]
) -> bool:
    """Return True if none of the keywords appear in output."""
    out_low = output.lower()
    return not any(kw.lower() in out_low for kw in keywords)

@staticmethod
def is_por_structure(
    output: str
) -> bool:
    """Return True if output contains POR structure keywords."""
    out_low = output.lower()
    # detect basic POR keywords
    return any(kw in out_low for kw in ["por", "resonance"])

@staticmethod
def evolution_index(
    E: List[float],
    S: List[float],
    weights: List[float]
) -> float:
    """
    Evolution index: weighted average of (E_i + S_i).
    """
    num = sum((e + s) * w for e, s, w in zip(E, S, weights))
    denom = sum(weights)
    return num / denom

@staticmethod
def por_firing_probability(
    I_q: float,
    E_m: float,
    R_def: float,
    theta: float
) -> bool:
    """
    Return True if I_q exceeds membrane potential plus refractory term.
    """
    return I_q > E_m + R_def

