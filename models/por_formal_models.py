import math import numpy as np from typing import List, Optional, Union from transformers import pipeline

class PoRModel: """ Core PoR (Point of Resonance) model calculations. """

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
def por_collapse_frequency(lambda_rate: float, t: float) -> float:
    """
    PoR_rate(t) = λ · e^(−λt)
    """
    if lambda_rate < 0 or t < 0:
        raise ValueError("Lambda rate and time must be non-negative.")
    return lambda_rate * math.exp(-lambda_rate * t)

@staticmethod
def por_firing_probability(I_q: float, E_m: float, R_def: float, theta: float) -> bool:
    """(I_q × E_m) / (R_def + 1) > θ"""
    denom = R_def + 1
    if denom == 0:
        raise ValueError("Denominator (R_def + 1) cannot be zero.")
    return (I_q * E_m) / denom > theta

@staticmethod
def refire_difference(E1: float, E2: float) -> float:
    """ΔE = |E1 - E2|"""
    return abs(E1 - E2)

@staticmethod
def self_coherence(reference_flow: float, delta_I_in: float, delta_I_out: float) -> float:
    """
    φ_C = reference_flow / (|ΔI_in| + |ΔI_out|)
    """
    denom = abs(delta_I_in) + abs(delta_I_out)
    if denom == 0:
        raise ZeroDivisionError("Sum of absolute changes in input/output flow cannot be zero.")
    return reference_flow / denom

@staticmethod
def gravity_tensor(grad_por_density: Union[List[float], np.ndarray], grad_por_entropy: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    Outer product of density and entropy gradients: G_{ij} = (∇ρ)_i · (∇η)_j
    """
    rho = np.asarray(grad_por_density, dtype=float)
    eta = np.asarray(grad_por_entropy, dtype=float)
    if rho.ndim != 1 or eta.ndim != 1 or rho.shape != eta.shape:
        raise ValueError("Gradient vectors must be 1-dimensional and of equal length.")
    return np.outer(rho, eta)

@staticmethod
def phase_gradient(k: float, E: float, S: float, gamma: float) -> float:
    """dΦ/dt = k · E · S^γ"""
    if S < 0 and not float(gamma).is_integer():
        raise ValueError("Semantic density S cannot be negative if gamma is not integer.")
    return k * E * (S ** gamma)

@staticmethod
def evolution_index(Q_list: List[float], S_list: List[float], t_list: List[float]) -> float:
    """
    Calculate and sum E for multiple (Q, S_q, t) tuples.
    """
    return sum(Q * S_q * t for Q, S_q, t in zip(Q_list, S_list, t_list))

@staticmethod
def is_por_null(text: str, keywords: List[str]) -> bool:
    """
    Return True if none of the keywords appear in the text.
    """
    lower = text.lower()
    return not any(kw.lower() in lower for kw in keywords)

@staticmethod
def is_por_structure(text: str, keywords: Optional[List[str]] = None) -> bool:
    """
    Check if text contains any PoR structure keywords.
    Defaults to ['por', 'resonance'].
    """
    if keywords is None:
        keywords = ["por", "resonance"]
    lower = text.lower()
    return any(kw.lower() in lower for kw in keywords)

