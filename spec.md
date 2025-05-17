# PoR/ΔE OSS Library Specification Draft

## Purpose
- Provide a reproducible library for PoR trigger and ΔE scoring

## Core Functions
- por_trigger(q, s, t, phi_C, D): PoR firing decision
- deltae_score(E1, E2): ΔE score calculation

## I/O Examples
- por_trigger: input (q, s, t, phi_C, D) → output (bool, score value)
- deltae_score: input (E1, E2) → output (ΔE value)

## Reference Formulas
- E' = q × s × t
- score = E' × φ_C
- ΔE = E2 - E1
