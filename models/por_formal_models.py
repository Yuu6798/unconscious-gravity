# models/por_formal_models.py

import math
import numpy as np
from typing import List, Union

class PoRModel:
    """Core PoR (Point of Resonance) model calculations."""

    @staticmethod
    def existence(Q: float, S_q: float, t: float) -> float:
        return Q * S_q * t

    @staticmethod
    def self_por_score(E_base: float, delta_E_over: float, Q_self_factor: float) -> float:
        return E_base + delta_E_over * Q_self_factor

    @staticmethod
    def mismatch(E: float, Q: float) -> float:
        return abs(E - Q)

    @staticmethod
    def semantic_gravity(por_freq: float, entropy: float) -> float:
        return por_freq * entropy

    @staticmethod
    def por_collapse_frequency(lam: float, t: float) -> float:
        """
        Collapse frequency: λ × e^(−λ·t)
        Args:
          lam: decay constant λ
          t:   elapsed time
        """
        return lam * math.exp(-lam * t)

    @staticmethod
    def por_firing_probability(I_q: float, E_m: float, R_def: float, theta: float) -> bool:
        denom = R_def + 1
        if denom == 0:
            raise ValueError("R_def + 1 cannot be zero.")
        return (I_q * E_m) / denom > theta

    @staticmethod
    def refire_difference(new_refire: float, old_refire: float) -> float:
        return abs(new_refire - old_refire)

    @staticmethod
    def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
        """
        ref_flow / (d_in + d_out), raises ZeroDivisionError if denominator is zero
        """
        total = d_in + d_out
        if total == 0:
            raise ZeroDivisionError("Sum of d_in and d_out cannot be zero.")
        return ref_flow / total

    @staticmethod
    def gravity_tensor(vec: List[float], weights: List[float]) -> float:
        return float(np.dot(np.array(vec), np.array(weights)))

    @staticmethod
    def phase_gradient(*args) -> float:
        if len(args) == 2:
            k, E = args
            return k * E
        if len(args) == 4:
            E, S, k, gamma = args
            if not isinstance(S, (int, float)):
                raise TypeError("S must be a number")
            if S < 0:
                raise ValueError("S must be non-negative")
            return k * E * (S ** gamma)
        raise TypeError("phase_gradient() expects either 2 or 4 arguments")

    @staticmethod
    def evolution_index(Q_list: List[float], S_list: List[float], t_list: List[float]) -> float:
        return float(np.sum(np.array(Q_list) * np.array(S_list) * np.array(t_list)))

    @staticmethod
    def is_por_null(text: str, keywords: List[str]) -> bool:
        low = text.lower()
        return not any(kw.lower() in low for kw in keywords)

    @staticmethod
    def is_por_structure(text: str) -> bool:
        low = text.lower()
        return "por" in low or "resonance" in low