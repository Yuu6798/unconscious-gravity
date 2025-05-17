def por_trigger(q, s, t, phi_C, D, theta=0.6):
    """PoR firing decision. Returns True/False based on the condition."""
    E_prime = q * s * t
    score = E_prime * phi_C
    triggered = (score * (1 - D)) > theta
    return {"E_prime": E_prime, "score": score, "triggered": triggered}


def deltae_score(E1, E2):
    """ΔE (energy change)"""
    return E2 - E1
