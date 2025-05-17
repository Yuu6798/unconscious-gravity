# PoR・ΔE OSS Library Specification Draft

## Purpose
- To make PoR trigger and ΔE score reproducible for anyone as a library

## Core functions
- por_trigger(q, s, t, phi_C, D): PoR firing decision
- deltae_score(E1, E2): ΔE score calculation

## I/O examples
- por_trigger: input (q, s, t, phi_C, D) → output (bool, score value)
- deltae_score: input (E1, E2) → output (ΔE value)

## Reference formulas
- E' = q × s × t
- score = E' × φ_C
- ΔE = E2 - E1
