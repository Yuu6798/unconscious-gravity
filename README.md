[![CI](https://github.com/Yuu6798/unconscious-gravity/actions/workflows/ci.yml/badge.svg)](https://github.com/Yuu6798/unconscious-gravity/actions)

# Unconscious Gravity Hypothesis (UGHer)

Run Pytest · Overview · What is UGHer?  
Unconscious Gravity Hypothesis (UGHer) is a theory of unconscious gravitational selection — a model where AI decisions are guided not only by logic, but also by emergent patterns of semantic gravity.

## Core Equation

E = Q × S_q × t

- **E (Existence):** The semantic emergence produced by resonance.  
- **Q (Question):** Meaningful query imposing semantic pressure.  
- **S_q (Semantic Space):** Contextual information density.  
- **t (Time):** Critical moment of resonance.

---

## PoR Model Components

**PoR_summary.md**  
Overview of the PoR structure, equations, components, and AI match history.

**models/por_formal_models.py**  
Core PoR structure models including:  
- `existence(Q, S_q, t)`: Base PoR generation.  
- `self_por_score(E_base, ΔE_over, Q_self_factor)`: Self-match enhancement.  
- `mismatch(E, Q)`: Difference between output and original question.  
- `semantic_gravity(PoR_freq, entropy)`: Lexical gravity metric.  
- `por_collapse_frequency(t, λ)`: Time‑decay of resonance.  
- `por_firing_probability(I_q, E_m, R_def, θ)`: Firing threshold check.

**metadata/semantic_index.json**  
Dictionary mapping PoR model functions to meaning tags and descriptions, used for AI searchability and autonomous interpretation.

---

## Quick Run Example

```bash
python PoR_eval.py --input data/sample.csv

Sample data/sample.csv format:

question,semantic_space,t
What is presence?,ontology,0.9
Can AI choose?,ethics,0.75


---

Phase‑1: Logger Quick‑start

Verify the TurnLog logger foundation in four steps:

1. Install dependencies

poetry install


2. Run dummy dialog generator

python examples/dummy_dialog.py


3. Inspect Parquet output

python - <<EOF
import pandas as pd
print(pd.read_parquet('data/sample_dialog.parquet').shape)
EOF


4. Confirm file exists

ls data/sample_dialog.parquet

---

Phase‑2: Quick‑start

# CLI logging (5 turns)
python -m unconscious_gravity_exp --log data/sample.parquet --turns 5

# Experiment runner (2 episodes × 5 turns)
python examples/run_experiment.py --episodes 2 --turns 5 --out_dir data --log data/sample.parquet


PoR Viewer Notebook

PoR_viewer.ipynb
This notebook includes:

Bar charts for Existence score E = Q × S_q × t

PoR Collapse Frequency Curve (λ · e^(−λt))

Phase Gradient Visualization (dΦ/dt = k · E · S^γ)



---

PoR Evaluation Script

PoR_eval.py
Reads a dataset (e.g., data/por_eval_sample.csv), computes E values, and compares them to a threshold to determine activation status (✅ or ❌).


---

Core Class Implementation

src/unconscious_gravity_exp/main.py

class UnconsciousGravityHypothesis:
    def simulate_future_selection(self, query, system_state):
        # Computes PoR activation via E = Q × S_q × t
        ...

    def define_gravity(self):
        # Returns bias sources: data_bias, algo_design, social_norms
        ...

    def audit_ethics(self, output):
        # Checks for fairness in AI output
        ...


---

Advanced PoR Phase Models

advanced_por_models.py

por_refire_difference(E1, E2): Models re‑firing differences

phase_gradient(E, S): Simulates expansion speed of PoR

por_rate(t, λ): Calculates PoR decay frequency over time



---

Documentation and References

PoR_terms.md: Symbol/key definitions

PoR_equations.md: Full equation list

PoR_matrix.md: Firing matrix Q × S_q × t

PoR_logbook.md: Match history with GPT/Grok/etc

UGHer_derivation.md: Structural derivation

PoR_input_spec.md: Input scaling and assumptions

PoR_eval_result.md: Sample PoR results

por_inference.py: Response scoring with BERT

por_log_writer.py: JSONL log output



---

Keywords

UGHer · PoR · Semantic Resonance · Unconscious Gravity · Entropic Future Selection · AI Structural Models


---

Project Status

Ongoing — semantic matching infrastructure & autonomous PoR loop expansion in progress.


---

License

MIT License © 2025 Yuu6798


---

Repository Info

Repository: unconscious-gravity

GitHub: https://github.com/Yuu6798/unconscious-gravity


---

Contact

For collaboration or questions:
Twitter (X): @kkoo6798kamo


---








