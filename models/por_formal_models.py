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
        """PDF of exponential distribution: lam * exp(-lam * t)"""
        return lam * math.exp(-lam * t)

    @staticmethod
    def phase_gradient(E: float, S: float, k: float = 1.0, gamma: float = 1.0) -> float:
        """phase gradient = k * E * S**gamma"""
        return k * E * S**gamma

    @staticmethod
    def gravity_tensor(v1: List[float], v2: List[float]) -> float:
        """gravity tensor (dot product)"""
        return sum(a * b for a, b in zip(v1, v2))

    @staticmethod
    def evolution_index(Qs: List[float], S_qs: List[float], ts: List[float]) -> float:
        """evolution index = Σ Q_i × S_q_i × t_i"""
        return sum(Q * S_q * t for Q, S_q, t in zip(Qs, S_qs, ts))

    @staticmethod
    def is_por_structure(output: str, tags: List[str]) -> bool:
        """Detect if any of the tags appears in the output string."""
        txt = output.lower()
        return any(tag.lower() in txt for tag in tags)

    @staticmethod
    def is_por_null(output: str, tags: List[str]) -> bool:
        """Return True if none of the tags appears in the output."""
        return not PoRModel.is_por_structure(output, tags)