# models/por_formal_models.py

import math
import numpy as np
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
        """Mismatch = |E - Q|"""
        return abs(E - Q)

    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        """grv = por_freq × entropy"""
        return por_freq * entropy

    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """
        Collapse frequency:
          λ · e^(−λ·t)
        """
        return lam * math.exp(-lam * t)

    @staticmethod
    def refire_difference(new_refire: float, old_refire: float) -> float:
        """Difference in refire rates/times."""
        return abs(new_refire - old_refire)

    @staticmethod
    def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
        """
        Self coherence:
          ref_flow / (d_in + d_out), or 0 if there is no flow
        """
        total = d_in + d_out
        if total == 0:
            return 0.0
        return ref_flow / total

    @staticmethod
    def gravity_tensor(vec: List[float], weights: List[float]) -> float:
        """Compute gravity tensor as dot product of two vectors."""
        return float(np.dot(np.array(vec), np.array(weights)))

    @staticmethod
    def phase_gradient(*args) -> float:
        """
        Phase gradient calculation.
        - 2 args: phase_gradient(a, b) = a × b
        - 4 args: phase_gradient(E, S, k, γ) = k × E × S**γ
        """
        if len(args) == 2:
            a, b = args
            return a * b
        if len(args) == 4:
            E, S, k, gamma = args
            if not isinstance(S, (int, float)):
                raise TypeError("S must be a number")
            if S < 0:
                raise ValueError("S must be non-negative")
            return k * E * S**gamma
        raise TypeError("phase_gradient() expects either 2 or 4 arguments")

    @staticmethod
    def evolution_index(Q_list: List[float], S_list: List[float], t_list: List[float]) -> float:
        """
        Evolution index: sum over i of (Q_i × S_i × t_i)
        """
        Q = np.array(Q_list)
        S = np.array(S_list)
        t = np.array(t_list)
        return float(np.sum(Q * S * t))

    @staticmethod
    def por_firing_probability(I_q: float, E_m: float, R_def: float, theta: float) -> bool:
        """
        Firing probability condition:
          True if (I_q × E_m − R_def) ≥ theta
        """
        return (I_q * E_m - R_def) >= theta

    @staticmethod
    def is_por_null(text: str, keywords: List[str]) -> bool:
        """
        Returns True if none of the keywords appear in text.
        """
        low = text.lower()
        return not any(kw.lower() in low for kw in keywords)

    @staticmethod
    def is_por_structure(text: str) -> bool:
        """
        Returns True if PoR–related keywords appear in text.
        Default keywords: "por", "resonance"
        """
        low = text.lower()
        for kw in ("por", "resonance"):
            if kw in low:
                return True
        return False