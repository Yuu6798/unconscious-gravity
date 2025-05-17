"""UGH3 core metrics calculations: PoR, ΔE, and grv.

This module provides simple helper functions to compute the primary
metrics used in the UGH3 model.
"""
from typing import Union

Number = Union[int, float]


def _ensure_numeric(*values: Number) -> None:
    """Validate that all supplied values are numeric.

    Raises:
        TypeError: if any value is not ``int`` or ``float``.
    """
    for v in values:
        if not isinstance(v, (int, float)):
            raise TypeError("Inputs must be numeric")


def calc_por(q: Number, s_q: Number, t: Number) -> float:
    """Calculate PoR existence ``E = Q × S_q × t``.

    Args:
        q: Question pressure ``Q``.
        s_q: Semantic resonance ``S_q``.
        t: Critical time ``t``.

    Returns:
        Product ``E``.

    Example:
        >>> calc_por(1.2, 0.8, 1.5)
        1.44
    """
    _ensure_numeric(q, s_q, t)
    return float(q * s_q * t)


def calc_delta_e(current_e: Number, previous_e: Number) -> float:
    """Compute energy gap ``ΔE = |E_current - E_previous|``.

    Args:
        current_e: Current energy value.
        previous_e: Previous energy value.

    Returns:
        Absolute difference ``ΔE``.

    Example:
        >>> calc_delta_e(2.5, 1.0)
        1.5
    """
    _ensure_numeric(current_e, previous_e)
    return float(abs(current_e - previous_e))


def calc_grv(por_freq: Number, entropy: Number) -> float:
    """Calculate lexical gravity ``grv = por_freq × entropy``.

    Args:
        por_freq: Frequency of PoR firing.
        entropy: Resonance entropy.

    Returns:
        Gravity value ``grv``.

    Example:
        >>> calc_grv(2.0, 0.8)
        1.6
    """
    _ensure_numeric(por_freq, entropy)
    return float(por_freq * entropy)
