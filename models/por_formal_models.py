import math
import numpy as np 
from typing import List, Optional, Union 
from transformers import pipeline

class PoRModel: """Core PoR (Point of Resonance) model calculations."""

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
def por_collapse_frequency(t: float, decay_rate: float) -> float:
    return decay_rate * math.exp(-decay_rate * t)

@staticmethod
def gravity_tensor(flow: List[float], weights: List[float]) -> float:
    return sum(f * w for f, w in zip(flow, weights))

@staticmethod
def phase_gradient(E: float, S: float, k: float = 1.0, gamma: float = 1.0) -> float:
    return k * E * (S ** gamma)

@staticmethod
def refire_difference(new_fire: float, old_fire: float) -> float:
    return new_fire - old_fire

@staticmethod
def self_coherence(ref_flow: float, d_in: float, d_out: float) -> float:
    total = d_in + d_out
    if total == 0:
        return 0.0
    return ref_flow / total

@staticmethod
def is_por_null(output: str, keywords: List[str]) -> bool:
    lower = output.lower()
    return not any(kw.lower() in lower for kw in keywords)

@staticmethod
def is_por_structure(output: str, keywords: Optional[List[str]] = None) -> bool:
    if keywords is None:
        keywords = ["por", "resonance"]
    lower = output.lower()
    return any(kw.lower() in lower for kw in keywords)

@staticmethod
def evolution_index(Qs: List[float], S_qs: List[float], ts: List[float]) -> float:
    return sum(Q * S_q * t for Q, S_q, t in zip(Qs, S_qs, ts))

