import math
import numpy as np
from typing import List, Optional, Union
from transformers import pipeline

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
    def por_collapse_frequency(t: float, lam: float) -> float:
        """Collapse frequency: lam × exp(-lam × t)"""
        return lam * math.exp(-lam * t)

    @staticmethod
    def phase_gradient(*args) -> float:
        """
        二つのシグネチャをサポート:
          1) phase_gradient(k, E) → k × E
          2) phase_gradient(E, S, k, gamma) → k × E × S**gamma
        """
        if len(args) == 2:
            k, E = args
            return k * E
        if len(args) == 4:
            E, S, k, gamma = args
            return k * E * (S ** gamma)
        raise TypeError("phase_gradient requires 2 or 4 arguments")

    @staticmethod
    def gravity_tensor(values: List[float], weights: List[float]) -> float:
        """Dot product of values and weights"""
        if len(values) != len(weights):
            raise ValueError("values and weights must have same length")
        return sum(v * w for v, w in zip(values, weights))

    @staticmethod
    def refire_difference(current: float, previous: float) -> float:
        """Difference between current and previous refire times"""
        return current - previous

    @staticmethod
    def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
        """
        Compute self-coherence as ref_flow / (d_in + d_out),
        if denominator is zero, return 0.0
        """
        denom = d_in + d_out
        if denom == 0:
            return 0.0
        return ref_flow / denom

    @staticmethod
    def evolution_index(Q_list: List[float], S_list: List[float], t_list: List[float]) -> float:
        """Sum of existence scores across lists: Σ (Q × S × t)"""
        if not (len(Q_list) == len(S_list) == len(t_list)):
            raise ValueError("Input lists must have same length")
        return sum(Q * S * t for Q, S, t in zip(Q_list, S_list, t_list))

    @staticmethod
    def is_por_null(output: str, tags: List[str]) -> bool:
        """Detect a 'null' PoR output from text or tags."""
        txt = output.strip().lower()
        if txt.startswith("no") or txt.startswith("null"):
            return True
        lower_tags = [t.lower() for t in tags]
        if "por" in lower_tags or "resonance" in lower_tags:
            return True
        return False