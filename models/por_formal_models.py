# models/por_formal_models.py

import math
from typing import List, Optional, Union


class PoRModel:
    """Core PoR (Point of Resonance) model calculations."""

    @staticmethod
    def existence(Q: float, S_q: float, t: float) -> float:
        """E = Q × S_q × t"""
        if not all(isinstance(val, (int, float)) for val in (Q, S_q, t)):
            raise TypeError("existence requires numeric inputs")
        return Q * S_q * t


    @staticmethod
    def self_por_score(E_base: float,
                       delta_E_over: float,
                       Q_self_factor: float) -> float:
        """E_self = E_base + ΔE_over × Q_self_factor"""
        if not all(isinstance(val, (int, float))
                   for val in (E_base, delta_E_over, Q_self_factor)):
            raise TypeError("self_por_score requires numeric inputs")
        return E_base + delta_E_over * Q_self_factor


    @staticmethod
    def mismatch(E: float, Q: float) -> float:
        """Mismatch = |E - Q|"""
        if not all(isinstance(val, (int, float)) for val in (E, Q)):
            raise TypeError("mismatch requires numeric inputs")
        return abs(E - Q)


    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        """grv = por_freq × entropy"""
        if not all(isinstance(val, (int, float)) for val in (por_freq, entropy)):
            raise TypeError("semantic_gravity requires numeric inputs")
        return por_freq * entropy


    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """λ·e^(−λt)"""
        if not all(isinstance(val, (int, float)) for val in (lam, t)):
            raise TypeError("por_collapse_frequency requires numeric inputs")
        return lam * math.exp(-lam * t)


    @staticmethod
    def por_firing_probability(I_q: float,
                                E_m: float,
                                R_def: float,
                                theta: float) -> bool:
        """Fire if I_q > E_m and R_def < theta."""
        if not all(isinstance(val, (int, float))
                   for val in (I_q, E_m, R_def, theta)):
            raise TypeError("por_firing_probability requires numeric inputs")
        return (I_q > E_m) and (R_def < theta)


    @staticmethod
    def refire_difference(prev: float, new: float) -> float:
        """Absolute difference between two refire times."""
        if not all(isinstance(val, (int, float)) for val in (prev, new)):
            raise TypeError("refire_difference requires numeric inputs")
        return abs(prev - new)


    @staticmethod
    def self_coherence(ref_flow: float,
                       d_in: float,
                       d_out: float) -> float:
        """Self coherence = ref_flow / (d_in + d_out)."""
        if not all(isinstance(val, (int, float))
                   for val in (ref_flow, d_in, d_out)):
            raise TypeError("self_coherence requires numeric inputs")
        return ref_flow / (d_in + d_out)


    @staticmethod
    def gravity_tensor(values: List[float],
                       weights: List[float]) -> float:
        """Σ (value_i × weight_i)"""
        if len(values) != len(weights):
            raise ValueError("values and weights must have same length")
        total = 0.0
        for v, w in zip(values, weights):
            if not isinstance(v, (int, float)) or not isinstance(w, (int, float)):
                raise TypeError("gravity_tensor requires numeric lists")
            total += v * w
        return total


    @staticmethod
    def phase_gradient(E: float,
                       S: float,
                       k: Optional[float] = None,
                       gamma: Optional[float] = None) -> float:
        """
        Phase gradient:
         - 2引数版: E × S
         - 4引数版: k × E × S^γ
        """
        # 型チェック
        if not isinstance(E, (int, float)):
            raise TypeError("E must be numeric")
        if not isinstance(S, (int, float)):
            raise TypeError("S must be numeric")

        # 2引数版
        if k is None and gamma is None:
            if S < 0:
                raise ValueError("S must be non-negative")
            return E * S

        # 4引数版
        if not isinstance(k, (int, float)):
            raise TypeError("k must be numeric")
        if not isinstance(gamma, (int, float)):
            raise TypeError("gamma must be numeric")

        if S < 0:
            raise ValueError("S must be non-negative")
        return k * E * (S ** gamma)


    @staticmethod
    def evolution_index(Qs: List[float],
                        S_qs: List[float],
                        ts: List[float]) -> float:
        """
        Evolution index = Σ (Q_i × S_q_i × t_i)
        """
        if not (len(Qs) == len(S_qs) == len(ts)):
            raise ValueError("Lists must have same length")
        total = 0.0
        for Q, S_q, t in zip(Qs, S_qs, ts):
            total += PoRModel.existence(Q, S_q, t)
        return total


    @staticmethod
    def is_por_null(text: str, keywords: List[str]) -> bool:
        """
        True if text contains none of the keywords.
        """
        if not isinstance(text, str):
            raise TypeError("text must be string")
        if not isinstance(keywords, list):
            raise TypeError("keywords must be list of strings")

        for kw in keywords:
            if not isinstance(kw, str):
                raise TypeError("each keyword must be string")
            if kw.lower() in text.lower():
                return False
        return True


    @staticmethod
    def is_por_structure(text: str) -> bool:
        """
        True if any of default keywords appear in text.
        """
        if not isinstance(text, str):
            raise TypeError("text must be string")

        default_keywords = ["por", "resonance"]
        for kw in default_keywords:
            if kw.lower() in text.lower():
                return True
        return False