# models/por_formal_models.py

import math
from typing import List, Optional

class PoRModel:
    """Core PoR (Point of Resonance) model calculations."""

    @staticmethod
    def existence(Q: float, S_q: float, t: float) -> float:
        """E = Q × S_q × t"""
        if not all(isinstance(x, (int, float)) for x in (Q, S_q, t)):
            raise TypeError("Q, S_q, and t must be numeric")
        return Q * S_q * t

    @staticmethod
    def self_por_score(E_base: float, delta_E_over: float, Q_self_factor: float) -> float:
        """E_self = E_base + ΔE_over × Q_self_factor"""
        if not all(isinstance(x, (int, float)) for x in (E_base, delta_E_over, Q_self_factor)):
            raise TypeError("E_base, delta_E_over, and Q_self_factor must be numeric")
        return E_base + delta_E_over * Q_self_factor

    @staticmethod
    def mismatch(E: float, Q: float) -> float:
        """Mismatch = |E - Q|"""
        if not all(isinstance(x, (int, float)) for x in (E, Q)):
            raise TypeError("E and Q must be numeric")
        return abs(E - Q)

    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        """grv = por_freq × entropy"""
        if not all(isinstance(x, (int, float)) for x in (por_freq, entropy)):
            raise TypeError("por_freq and entropy must be numeric")
        return por_freq * entropy

    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """λ × exp(−λ t)"""
        if not all(isinstance(x, (int, float)) for x in (lam, t)):
            raise TypeError("lam and t must be numeric")
        return lam * math.exp(-lam * t)

    @staticmethod
    def refire_difference(prev_fire: float, curr_fire: float) -> float:
        """Difference between two firing times"""
        if not all(isinstance(x, (int, float)) for x in (prev_fire, curr_fire)):
            raise TypeError("prev_fire and curr_fire must be numeric")
        return prev_fire - curr_fire

    @staticmethod
    def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
        """Coherence = ref_flow / (d_in + d_out)"""
        if not all(isinstance(x, (int, float)) for x in (ref_flow, d_in, d_out)):
            raise TypeError("ref_flow, d_in, and d_out must be numeric")
        denom = d_in + d_out
        return ref_flow / denom  # ZeroDivisionError if denom == 0

    @staticmethod
    def gravity_tensor(a: List[float], b: List[float]) -> float:
        """Gravity tensor = Σ a_i × b_i"""
        if not (isinstance(a, list) and isinstance(b, list) and len(a) == len(b)):
            raise ValueError("a and b must be lists of equal length")
        total = 0.0
        for x, y in zip(a, b):
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise TypeError("Elements of a and b must be numeric")
            total += x * y
        return total

    @staticmethod
    def phase_gradient(E: float, S: float, k: Optional[float] = None, gamma: Optional[float] = None) -> float:
        """
        位相勾配。
        2 引数版: E × S
        4 引数版: k × E × (S ** gamma)
        """
        if not isinstance(E, (int, float)) or not isinstance(S, (int, float)):
            raise TypeError("E and S must be numeric")
        # 2 引数版
        if k is None and gamma is None:
            return E * S
        # 片方だけ指定はエラー
        if k is None or gamma is None:
            raise TypeError("must supply both k and gamma")
        if not isinstance(k, (int, float)) or not isinstance(gamma, (int, float)):
            raise TypeError("k and gamma must be numeric")
        return k * E * (S ** gamma)

    @staticmethod
    def is_por_null(output: str, keywords: List[str]) -> bool:
        """Null 出力判定: キーワードのいずれかを含むか"""
        if not isinstance(output, str) or not isinstance(keywords, list):
            raise TypeError("output must be str and keywords must be list of str")
        return any(kw in output for kw in keywords)

    @staticmethod
    def is_por_structure(output: str) -> bool:
        """構造検出: 'resonance' または 'PoR' の有無で判定"""
        if not isinstance(output, str):
            raise TypeError("output must be str")
        return ("resonance" in output) or ("PoR" in output)

    @staticmethod
    def evolution_index(Q: List[float], S_q: List[float], R_def: List[float]) -> float:
        """Evolution index = Σ (Q_i × S_q_i × R_def_i)"""
        if not (isinstance(Q, list) and isinstance(S_q, list) and isinstance(R_def, list)):
            raise TypeError("Q, S_q, and R_def must be lists")
        if not (len(Q) == len(S_q) == len(R_def)):
            raise ValueError("Q, S_q, and R_def must be same length")
        total = 0.0
        for q, s, r in zip(Q, S_q, R_def):
            if not isinstance(q, (int, float)) or not isinstance(s, (int, float)) or not isinstance(r, (int, float)):
                raise TypeError("Elements of Q, S_q, R_def must be numeric")
            total += q * s * r
        return total

    @staticmethod
    def por_firing_probability(I_q: float, E_m: float, R_def: float, theta: float) -> bool:
        """
        発火判定: (I_q / E_m) × R_def >= theta なら True
        """
        if not all(isinstance(x, (int, float)) for x in (I_q, E_m, R_def, theta)):
            raise TypeError("I_q, E_m, R_def, theta must be numeric")
        return (I_q / E_m) * R_def >= theta