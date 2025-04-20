import math
from typing import List, Optional, Union

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
        """Mismatch = |E - Q|"""
        return abs(E - Q)

    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        """Semantic gravity = por_freq × entropy"""
        return por_freq * entropy

    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """
        Collapse frequency: λ · exp(−λ t)
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
        ・2 引数版: E × S
        ・3 引数版: k × S
        ・4 引数版: k × E × S^γ
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

        # その他（引数の組み合わせエラー）
        raise TypeError("invalid arguments for phase_gradient")

    @staticmethod
    def gravity_tensor(
        por_freqs: Union[List[float], float],
        entropies: Union[List[float], float]
    ) -> float:
        """
        重力テンソル: 各要素の semantic_gravity を合計
        """
        if isinstance(por_freqs, list):
            return sum(
                PoRModel.semantic_gravity(f, s)
                for f, s in zip(por_freqs, entropies)
            )
        else:
            return PoRModel.semantic_gravity(por_freqs, entropies)

    @staticmethod
    def evolution_index(
        por_freqs: List[float],
        entropies: List[float],
        time_steps: List[float]
    ) -> float:
        """
        進化指数: 各時間ステップにおける重力テンソルの差を合計
        """
        values = [
            PoRModel.gravity_tensor(
                [por_freqs[i], por_freqs[i+1]],
                [entropies[i], entropies[i+1]]
            )
            for i in range(len(time_steps)-1)
        ]
        return sum(values)

    @staticmethod
    def refire_difference(I_q: float, last_fire: float) -> float:
        """Refire difference = I_q − last_fire"""
        return I_q - last_fire

    @staticmethod
    def self_coherence(
        ref_flow: float,
        d_in: float,
        d_out: float
    ) -> float:
        """
        Self coherence = ref_flow / (d_in + d_out)
        d_in + d_out がゼロなら ZeroDivisionError
        """
        return ref_flow / (d_in + d_out)

    @staticmethod
    def is_por_null(
        output: str,
        keywords: List[str]
    ) -> bool:
        """PoR 構造が検出されない場合 True"""
        return all(kw.lower() not in output.lower() for kw in keywords)

    @staticmethod
    def por_firing_probability(
        I_q: float,
        E_m: float,
        R_def: float,
        theta: float
    ) -> bool:
        """
        発火確率:
        True if I_q − E_m − R_def > θ else False
        """
        return (I_q - E_m - R_def) > theta

    @staticmethod
    def is_por_structure(output: str) -> bool:
        """
        PoR 構造が検出されたか判定
        (semantic, gravity, resonance の3語がすべて含まれるか)
        """
        text = output.lower()
        return all(word in text for word in ["semantic", "gravity", "resonance"])