# por_formal_models.py

import math
from typing import List, Optional, Union

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
        """λ·e^(−λt)"""
        return lam * math.exp(-lam * t)

    @staticmethod
    def refire_difference(prev: float, curr: float) -> float:
        """差分としての再発火時間"""
        return prev - curr

    @staticmethod
    def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
        """
        自己コヒーレンス = ref_flow / (d_in + d_out)
        (d_in + d_out)=0のときは ZeroDivisionError を発生させる
        """
        return ref_flow / (d_in + d_out)

    @staticmethod
    def gravity_tensor(values: List[float], weights: List[float]) -> float:
        """内積によるテンソル効果"""
        if len(values) != len(weights):
            raise ValueError("length mismatch")
        return sum(v * w for v, w in zip(values, weights))

    @staticmethod
    def phase_gradient(E: float, S: float, k: Optional[float] = None, gamma: Optional[float] = None) -> float:
        """
        位相勾配。2 引数版: k × S,
        4 引数版: k × E × S^γ
        """
        # 2 引数版
        if k is None and gamma is None:
            raise TypeError("must supply at least k")
        if gamma is None:
            # signature: phase_gradient(k, S)
            return E * S
        # 4 引数版
        return k * E * (S ** gamma)

    @staticmethod
    def por_firing_probability(I_q: float, E_m: float, R_def: float, theta: float) -> bool:
        """
        発火確率判定 (例): I_q + E_m − R_def >= θ なら True
        """
        return (I_q + E_m - R_def) >= theta

    @staticmethod
    def evolution_index(Q: List[float], S_q: List[float], R: List[float]) -> float:
        """
        進化指数 = 重み付き Q の合計
        """
        if not (len(Q) == len(S_q) == len(R)):
            raise ValueError("length mismatch")
        return sum(q * sq for q, sq in zip(Q, S_q))

    @staticmethod
    def is_por_null(output: str, keywords: List[str]) -> bool:
        """
        Null 扱い判定: output にキーワードが含まれなければ True
        """
        return not any(kw in output for kw in keywords)

    @staticmethod
    def is_por_structure(output: str) -> bool:
        """
        PoR 構造検出: "resonance" 等が文字列に含まれるか
        """
        return "resonance" in output.lower() or "por" in output.lower()