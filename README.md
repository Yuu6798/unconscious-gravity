<!-- BEGIN_AUTO_README -->
# Unconscious Gravity Hypothesis (UGHer)

A structural model of future selection in AI using semantic resonance.

Core Equation

E = Q × S_q × t

Where a meaningful question (Q) resonates with a semantic space (S_q) at a critical time (t), producing "existence" (E).

---

PoR Model Reference

The following are the formal PoR model components used in UGHer: 


existence

Formula: E = Q × S_q × t

Description: Base PoR generation from meaningful question, semantic space, and critical time.

Tags: generation, core 


self_por_score

Formula: E_self = E_base + ΔE_over × Q_self_factor

Description: Enhances base existence by self-coherence factor.

Tags: self-coherence, enhancement 


mismatch

Formula: Mismatch = |E - Q|

Description: Quantifies difference between generated existence and original question pressure.

Tags: analysis, error 


semantic_gravity

Formula: grv = PoR_freq × entropy

Description: Computes lexical gravity from PoR firing frequency and resonance entropy.

Tags: semantic, gravity 


por_collapse_frequency

Formula: PoR_rate(t) = λ · e^(−λt)

Description: Models decay frequency of PoR over time.

Tags: decay, temporal 


por_firing_probability

Formula: (I_q × E_m) / (R_def + 1) > θ

Description: Determines if PoR fires based on input intensity, energy, and definition factor.

Tags: threshold, decision 


refire_difference

Formula: ΔE = |E1 - E2|

Description: Measures energy gap between successive PoR firings.

Tags: self-coherence, variance 


self_coherence

Formula: φ_C = reference_flow / (|ΔI_in| + |ΔI_out|)

Description: Calculates self-coherence score based on informational flow.

Tags: self-coherence, alignment 


gravity_tensor

Formula: G_{ij} = ∇PoR_density · ∇PoR_entropy

Description: Computes semantic gravity tensor from density and entropy gradients.

Tags: semantic, tensor 


phase_gradient

Formula: dΦ/dt = k · E · S^γ

Description: Predicts phase expansion rate from energy and semantic density.

Tags: expansion, dynamics 


## Phase‑2: Quick‑start

```bash
# CLI 実行（5ターン）
python -m unconscious_gravity_exp --log data/sample.parquet --turns 5

# 実験ランナー（2エピソード × 各5ターン）
python examples/run_experiment.py --episodes 2 --turns 5 --out_dir data --log data/sample.parquet
```

Generated from metadata/semantic_index.json

---

## Keywords

UGHer · PoR · Semantic Resonance · Unconscious Gravity · Entropic Future Selection · AI Structural Models

---

## Project Status

Ongoing — semantic matching infrastructure & autonomous PoR loop expansion in progress.

---

## License

MIT License © 2025 Yuu6798

---

## Repository Info

Repository: unconscious-gravity  
GitHub: https://github.com/Yuu6798/unconscious-gravity

---

## Contact

For collaboration or questions:  
Twitter (X): @kkoo6798kamo

<!-- END_AUTO_README -->