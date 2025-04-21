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
    def por_collapse_frequency(lam: float, t: float) -> float:
        """Collapse frequency: λ · exp(−λ t)"""
        return lam * math.exp(-lam * t)

    @staticmethod
    def phase_gradient(
        E: float,
        S: float,
        k: Optional[float] = None,
        gamma: Optional[float] = None
    ) -> float:
        """
        Phase gradient:
        - 2-arg: E × S
        - 3-arg: k × S
        - 4-arg: k × E × S^γ
        """
        if S < 0:
            raise ValueError("entropy must be non-negative")

        # 2-arg
        if k is None and gamma is None:
            return E * S

        # 3-arg
        if k is not None and gamma is None:
            return k * S

        # 4-arg
        if k is not None and gamma is not None:
            return k * E * (S ** gamma)

        raise TypeError("invalid arguments for phase_gradient")

    @staticmethod
    def gravity_tensor(por_freqs: List[float], entropies: List[float]) -> float:
        """Gravity tensor: Σ por_freq[i] × entropy[i]"""
        return sum(f * s for f, s in zip(por_freqs, entropies))

    @staticmethod
    def refire_difference(new_val: float, old_val: float) -> float:
        """Absolute difference between new and old value"""
        return abs(new_val - old_val)

    @staticmethod
    def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
        """Self coherence = ref_flow / (d_in + d_out)"""
        return ref_flow / (d_in + d_out)

    @staticmethod
    def por_firing_probability(I_q: float, E_m: float, R_def: float, theta: float) -> bool:
        """
        Firing if (I_q * E_m / R_def) > theta.
        If R_def == 0, returns False.
        """
        if R_def == 0:
            return False
        return (I_q * E_m / R_def) > theta

    @staticmethod
    def evolution_index(
        Q_list: List[float],
        S_list: List[float],
        t_list: List[float]
    ) -> float:
        """Evolution index = Σ Q_i × S_i × t_i"""
        return sum(q * s * t for q, s, t in zip(Q_list, S_list, t_list))

    @staticmethod
    def is_por_null(output: str, keywords: List[str]) -> bool:
        """Returns True if none of keywords appear in output"""
        lower = output.lower()
        return not any(kw.lower() in lower for kw in keywords)

    @staticmethod
    def is_por_structure(output: str) -> bool:
        """Returns True only if 'semantic', 'gravity', and 'resonance' are all present"""
        lower = output.lower()
        return all(word in lower for word in ["semantic", "gravity", "resonance"])