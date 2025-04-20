# models/por_formal_models.py

import math
from typing import List

class PoRModel:
    """Core PoR (Point of Resonance) model calculations."""

    @staticmethod
    def existence(Q: float, S_q: float, t: float) -> float:
        """E = Q × S_q × t"""
        return Q * S_q * t

    @staticmethod
    def self_por_score(E_base: float, delta_E_over: float, Q_self_factor: float) -> float:
        """E_self = E_base + ΔE_over × Q_self_factor"""
        return E_base + delta_E_over * Q_self_factor

    @staticmethod
    def mismatch(E: float, Q: float) -> float:
        """Mismatch = |E − Q|"""
        return abs(E - Q)

    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        """grv = por_freq × entropy"""
        return por_freq * entropy

    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """
        Collapse frequency: λ · e^(−λt)
        signature: por_collapse_frequency(lam, t)
        """
        return lam * math.exp(-lam * t)

    @staticmethod
    def gravity_tensor(positions: List[float], weights: List[float]) -> float:
        """
        重み付き和:
        gravity_tensor([p1, p2, …], [w1, w2, …]) = Σ pi × wi
        """
        if len(positions) != len(weights):
            raise ValueError("positions and weights must have same length")
        total = 0.0
        for p, w in zip(positions, weights):
            total += p * w
        return total

    @staticmethod
    def phase_gradient(E: float, S: float) -> float:
        """
        2 引数版: E × S
        signature: phase_gradient(E, S)
        """
        return E * S

    @staticmethod
    def evolution_index(values: List[float], factors: List[float], indices: List[float]) -> float:
        """
        進化指標:
        evolution_index([v1, v2, …], [f1, f2, …], [i1, i2, …])
          = Σ vk × fk × ik
        """
        if not (len(values) == len(factors) == len(indices)):
            raise ValueError("All input lists must have the same length")
        total = 0.0
        for v, f, i in zip(values, factors, indices):
            total += v * f * i
        return total

    @staticmethod
    def por_firing_probability(I_q: float, E_m: float, R_def: float, theta: float) -> bool:
        """
        発火確率判定:
        R_def が 0 の場合は False を返す。
        それ以外は I_q ≥ (E_m / R_def) × theta なら True、そうでなければ False。
        """
        if R_def == 0:
            return False
        return I_q >= (E_m / R_def) * theta