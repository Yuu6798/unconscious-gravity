# Canonical Compatibility

This repository keeps PoR/ΔE/grv theory expressions as research artifacts.

Operational scoring/verdict behavior is defined in:

- `Yuu6798/ugh-audit-core/docs/canonical_metrics_contract.md`

Positioning:

- Here: `metric_mode="research_variant"` (theory-oriented formulas).
- Production audit and verdict: `ugh-audit-core` operational contract.

Guardrails:

- Do not publish incompatible formulas as plain production `delta_e`.
- Use explicit method labels when exporting metrics:
  - `metric_mode`
  - `delta_e_method`
  - `por_method`
  - `grv_method`
