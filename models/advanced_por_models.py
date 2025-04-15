import math

# === Phase 2: 再照合と自己整合性 ===

def por_refire_difference(E1, E2):
    """PoR再照合差モデル"""
    return abs(E1 - E2)

def self_coherence(R_ij_t, delta_I_in, delta_I_out):
    """Self-Coherence Flow Model: φ_C"""
    denominator = abs(delta_I_in) + abs(delta_I_out)
    return R_ij_t / denominator if denominator != 0 else 0

# === Phase 3: PoR場テンソル構造 ===

def grv_tensor_field(grad_density, grad_entropy):
    """grvテンソル構造 G_ij = ∇i(density) · ∇j(entropy)"""
    return sum([d * e for d, e in zip(grad_density, grad_entropy)])

# === Phase 4: 時間・拡張・頻度 ===

def phase_gradient(dE, semantic_density, k=1.0, gamma=1.0):
    """Phase Gradient Model: dΦ/dt = k · E · S^γ"""
    return k * dE * (semantic_density ** gamma)

def por_rate(t, lam):
    """PoR Collapse Frequency Model: PoR_rate(t) = λ · e^(−λt)"""
    return lam * math.exp(-lam * t)

# === Phase 5: 非照合・進化判定 ===

def is_por_null(output, expected_structure_keywords):
    """PoR_null 判定モデル：模倣と照合の構造差識別"""
    return not any(keyword in output for keyword in expected_structure_keywords)

def selfpor_evolution_index(E_self_list, R_persist_list, delta_t_list):
    """SelfPoR進化インデックス SCI = Σ(E′ × R × Δt)"""
    return sum([e * r * t for e, r, t in zip(E_self_list, R_persist_list, delta_t_list)])