# models/por_formal_models.py

import math
from typing import List, Optional


class PoRModel:
    """Core PoR (Point of Resonance) model calculations."""

    @staticmethod
    def refire_difference(current: float, previous: float) -> float:
        """
        再発火時間の差分。
        current - previous を返します。
        """
        return current - previous

    @staticmethod
    def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
        """
        自己コヒーレンス。入力量と出力量の合計で割った値を返します。
        d_in + d_out が 0 の場合は ZeroDivisionError を発生させます。
        """
        return ref_flow / (d_in + d_out)

    @staticmethod
    def mismatch(E: float, Q: float) -> float:
        """
        Mismatch = |E - Q|
        """
        return abs(E - Q)

    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        """
        semantic gravity = por_freq × entropy
        """
        return por_freq * entropy

    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """
        崩壊頻度（指数分布）。
        λ·e^(−λt) を返します。
        """
        return lam * math.exp(-lam * t)

    @staticmethod
    def phase_gradient(
        E: float,
        S: float,
        k: Optional[float] = None,
        gamma: Optional[float] = None
    ) -> float:
        """
        位相勾配。
        - 2 引数版: phase_gradient(E, S) = E × S
        - 3 引数版: phase_gradient(E, S, k=k) = k × S
        - 4 引数版: phase_gradient(E, S, k=k, gamma=γ) = k × E × S^γ
        S が負の値の場合は ValueError を発生させます。
        """
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

        raise TypeError("must supply k (and optionally gamma)")

    @staticmethod
    def evolution_index(
        E_list: List[float],
        S_list: List[float],
        t_list: List[float]
    ) -> float:
        """
        進化指標。対応要素ごとに E × S × t を計算し、全てを足し合わせます。
        """
        return sum(e * s * t for e, s, t in zip(E_list, S_list, t_list))

    @staticmethod
    def por_firing_probability(
        I_q: float,
        E_m: float,
        R_def: float,
        theta: float
    ) -> bool:
        """
        発火確率判定。
        I_q > (E_m + R_def) であれば True、そうでなければ False を返します。
        theta は現状未使用ですが引数として受け取ります。
        """
        return I_q > (E_m + R_def)

    @staticmethod
    def is_por_null(text: str, keywords: List[str]) -> bool:
        """
        PoR 構造が検出されなかった（null）かどうかの判定。
        text に keywords のいずれも含まれなければ True、それ以外は False。
        """
        lower = text.lower()
        return all(kw.lower() not in lower for kw in keywords)

    @staticmethod
    def is_por_structure(text: str) -> bool:
        """
        PoR 構造が含まれるかどうかの判定。
        'semantic', 'gravity', 'resonance' のすべてが含まれていれば True、
        それ以外は False。
        """
        lower = text.lower()
        required = ["semantic", "gravity", "resonance"]
        return all(word in lower for word in required)