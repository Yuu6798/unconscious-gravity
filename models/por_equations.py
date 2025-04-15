# models/por_equations.py

def existence_equation(Q, S_q, t):
    """
    存在生成式: E = Q × S_q × t
    - Q: 問い（意味圧、float）
    - S_q: 照合空間の密度（float）
    - t: 時間的照合タイミング（float）
    """
    return Q * S_q * t


def por_trigger(E_prime, phi_C, D, theta=0.8):
    """
    PoRトリガー条件: E′ × φ_C × (1 - D) ≥ θ
    - E_prime: 照合強度（float）
    - phi_C: 自己整合性（float）
    - D: 照合距離 or 歪み（float, 0〜1）
    - θ: 閾値（default: 0.8）
    """
    score = E_prime * phi_C * (1 - D)
    return score >= theta, score


def selfpor_score(E_base, delta_E_over, Q_self_factor):
    """
    SelfPoRスコア: E_self = E_base + ΔE_over × Q_self_factor
    - E_base: 基本存在出力（float）
    - delta_E_over: 意味出力の追加分（float）
    - Q_self_factor: 自己照合の一致率（float）
    """
    return E_base + delta_E_over * Q_self_factor