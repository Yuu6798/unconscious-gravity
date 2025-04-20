# models/por_formal_models.py

import math
from typing import List, Optional


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
        """Mismatch = |E - Q|"""
        return abs(E - Q)

    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        """Semantic gravity = por_freq × entropy"""
        return por_freq * entropy

    @staticmethod
    def gravity_tensor(por_freqs: List[float], entropies: List[float]) -> float:
        """Gravity tensor: sum of semantic gravities"""
        return sum(f * s for f, s in zip(por_freqs, entropies))

    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """Collapse frequency λ·e^(−λt)"""
        return lam * math.exp(-lam * t)

    @staticmethod
    def por_firing_probability(I_q: float,
                               E_m: float,
                               R_def: float,
                               theta: float) -> bool:
        """
        Firing probability:
        True if (I_q * E_m / R_def) ≥ θ, False if R_def == 0 or below threshold
        """
        if R_def == 0:
            return False
        return (I_q * E_m / R_def) >= theta

    @staticmethod
    def phase_gradient(E: float,
                       S: float,
                       k: Optional[float] = None,
                       gamma: Optional[float] = None) -> float:
        """
        Phase gradient:
        2-arg version: E × S
        3-arg version: k × S
        4-arg version: k × E × S^γ
        """
        # エントロピー S が負ならエラー
        if S < 0:
            raise ValueError("entropy must be non-negative")

        # 2 引数版
        if k is None and gamma is None:
            return E * S

        # 3 引数版
        if k is not None and gamma is None:
            return k * S

        # 4 引数版
        if k is not None and gamma is not None:
            return k * E * (S ** gamma)

        # 引数不足
        raise TypeError("must supply k (and optionally gamma)")

    @staticmethod
    def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
        """Self coherence: ref_flow / (d_in + d_out)"""
        return ref_flow / (d_in + d_out)

    @staticmethod
    def refire_difference(I_q: float, threshold: float) -> float:
        """Difference between refire rate and threshold"""
        return abs(I_q - threshold)

    @staticmethod
    def evolution_index(existences: List[float],
                        Qs: List[float],
                        ts: List[float]) -> float:
        """
        Evolution index: sum(existence × Q × t) over all time steps
        """
        return sum(e * q * t for e, q, t in zip(existences, Qs, ts))

    @staticmethod
    def is_por_null(text: str, labels: List[str]) -> bool:
        """
        Return True if the model output indicates no structure
        (e.g. contains 'no structure')
        """
        return "no structure" in text.lower()

    @staticmethod
    def is_por_structure(text: str) -> bool:
        """
        Return True if the text indicates PoR structure was detected
        (e.g. mentions 'resonance')
        """
        lowered = text.lower()
        return "resonance" in lowered