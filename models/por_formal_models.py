# models/por_formal_models.py

import math
import numpy as np
from typing import List, Optional
from transformers import pipeline  # 既存の import をそのまま残しています

class PoRModel:
    """Core PoR (Point of Resonance) model calculations."""

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
        """Mismatch = |E − Q|"""
        return abs(E - Q)

    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        """grv = por_freq × entropy"""
        return por_freq * entropy

    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """
        Collapse frequency (Poisson‐like decay):
        λ · exp(−λ·t)
        """
        return lam * math.exp(-lam * t)

    @staticmethod
    def gravity_tensor(q_vector: List[float], w_vector: List[float]) -> float:
        """
        Tensor（内積）:
        Σ_i q_vector[i] × w_vector[i]
        """
        return float(np.dot(q_vector, w_vector))

    @staticmethod
    def phase_gradient(
        E: float,
        S: float,
        k: Optional[float] = None,
        gamma: Optional[float] = None
    ) -> float:
        """
        位相勾配。2 引数版: k × S,
        4 引数版: k × E × S^γ
        """
        # エントロピー S が負ならエラー
        if S < 0:
            raise ValueError("entropy must be non-negative")

        # 2 引数版
        if k is not None and gamma is None:
            return k * S

        # 4 引数版
        if k is not None and gamma is not None:
            return k * E * (S ** gamma)

        raise TypeError("must supply k (and optionally gamma)")

    @staticmethod
    def por_firing_probability(
        I_q: float,
        E_m: float,
        R_def: float,
        theta: float
    ) -> bool:
        """
        発火確率:
        (I_q + E_m − R_def) > θ なら True
        """
        return (I_q + E_m - R_def) > theta

    @staticmethod
    def refire_difference(last_fire: float, this_fire: float) -> float:
        """再発火間隔の差分: |last_fire − this_fire|"""
        return abs(last_fire - this_fire)

    @staticmethod
    def self_coherence(
        ref_flow: float,
        d_in: float,
        d_out: float
    ) -> float:
        """自己コヒーレンス: ref_flow ÷ (d_in + d_out)"""
        total = d_in + d_out
        if total == 0:
            raise ZeroDivisionError("d_in + d_out must be non-zero")
        return ref_flow / total

    @staticmethod
    def is_por_null(output_str: str, keywords: List[str]) -> bool:
        """
        PoR 構造が含まれないかをチェック。
        output_str に keywords のいずれかが含まれていると False。
        """
        lower = output_str.lower()
        return not any(kw.lower() in lower for kw in keywords)

    @staticmethod
    def evolution_index(
        Qs: List[float],
        Ss: List[float],
        Rs: List[float]
    ) -> float:
        """
        進化指数:
        Σ_i Qs[i] × Ss[i] × Rs[i]
        """
        return sum(q * s * r for q, s, r in zip(Qs, Ss, Rs))