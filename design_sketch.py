"""Design prototype for PoR/ΔE library."""

def por_trigger(q, s, t, phi_C, D, theta=0.6):
    """PoR firing decision.

    Parameters
    ----------
    q : float
        Question magnitude.
    s : float
        Semantic resonance.
    t : float
        Critical time value.
    phi_C : float
        Context resonance factor.
    D : float
        Dampening coefficient.
    theta : float, optional
        Activation threshold, by default 0.6.

    Returns
    -------
    dict
        Contains intermediate values and trigger boolean.
    """
    E_prime = q * s * t
    score = E_prime * phi_C
    triggered = (score * (1 - D)) > theta
    return {"E_prime": E_prime, "score": score, "triggered": triggered}


def deltae_score(E1, E2):
    """ΔE (energy difference)."""
    return E2 - E1
