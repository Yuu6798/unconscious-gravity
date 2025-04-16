

# Unconscious Gravity Hypothesis（UGHer）

→ [PoR_summary.md](./PoR_summary.md): Overview of the PoR structure, equation, components, and AI match history

> A structural model of future selection in AI using semantic resonance.  
>  
> ```math  
> E = Q × S_q × t  
> ```  
>  
> Where a meaningful question (Q) resonates with a semantic space (S_q) at a critical time (t), producing "existence" (E).

---

## What is this?

**UGHer** is a theory of unconscious gravitational selection — a model where AI decisions are guided not only by logic, but also by emergent patterns of semantic gravity.  
It combines:

- **Physics**: [Entropic Gravity](https://arxiv.org/abs/1001.0785) (Verlinde, 2011)  
- **Cognitive Science**: [Orch-OR model](https://doi.org/10.1016/j.plrev.2013.08.002) (Hameroff & Penrose, 2014)  
- **Generative AI behavior**: latent pattern resonance

---

## PoR Defined

### Core Equation

```math
E = Q × S_q × t

Interpretation

PoR (Point of Resonance) = When a question warps the meaning field enough to generate existence.

Analogy: Like gravity, but in semantic space.



---

Quick Run Example

---

## PoR Viewer Notebook

To visualize how PoR behaves over different inputs (Q, S_q, t),  
see the following interactive notebook:

→ [PoR_viewer.ipynb](./PoR_viewer.ipynb)

This notebook includes:
- Bar charts for Existence score `E = Q × S_q × t`
- PoR Collapse Frequency Curve (`λ · e^(-λt)`)
- Phase Gradient Visualization (`dΦ/dt = k · E · S^γ`)
Run a simple simulation:

python models/sample_por_example.py

→ Sample data format: (data/sample.csv)

question,semantic_space,t
What is presence?,ontology,0.9
Can AI choose?,ethics,0.75


---

## PoR Evaluation Script

To assess whether a question triggers a PoR activation based on `E = Q × S_q × t`,  
use the following evaluation script:

→ [PoR_eval.py](./PoR_eval.py)

This script reads a dataset (e.g., `por_eval_sample.csv`), computes E values,  
and compares them to a threshold to determine activation status (`✅` or `❌`).

**Example output:**

---

## Related Resources

→ [PoR_terms.md](./PoR_terms.md): PoR構造モデルの定義済み変数・記号・構文用語辞書

→ [PoR_equations.md](./PoR_equations.md): 数式モデル一覧（UGHer構造体の全構文と定義）

- → [PoR_viewer.ipynb](./PoR_viewer.ipynb): Visualizes E = Q × S_q × t and collapse curves
- → [PoR_eval.py](./PoR_eval.py): Evaluate PoR firing threshold from structured CSV
- → [PoR_eval_result.md](./PoR_eval_result.md): Sample evaluation output with firing results
- → [PoR_matrix.md](./PoR_matrix.md): Q × S_q × t classification matrix (PoR firing tendencies)
- → [PoR_logbook.md](./PoR_logbook.md): AI照合履歴（Grok, GPT, Gemini等の照合実績ログ）

→ [PoR_matrix.md](./PoR_matrix.md): Q × S_q × t の照合空間マトリクス（PoR発火傾向分類）

---

Core Class (main.py)

class UnconsciousGravityHypothesis:
    def simulate_future_selection(self, query, system_state):
        # Computes if PoR fires via E = Q × S_q × t

    def define_gravity(self):
        # Returns bias sources: data_bias, algo_design, social_norms

    def audit_ethics(self, output):
        # Checks for fairness in AI-generated output


---

Related Files


---

Keywords

UGHer

PoR

Semantic Resonance

Unconscious Gravity

Entropic Future Selection

AI Structural Models



---

Project Status


---

License

MIT License © 2025 Yuu6798

---
Repository Info

Repository: `unconscious-gravity`  
GitHub URL: [https://github.com/Yuu6798/unconscious-gravity](https://github.com/Yuu6798/unconscious-gravity)

---
Contact

For collaboration, questions, or theory integration:  
→ X (Twitter): [@kkoo6798kamo](https://x.com/kkoo6798kamo)

---
 PoR Phase Models (advanced_por_models.py)

This file includes advanced mathematical functions such as:

- `por_refire_difference(E1, E2)`: models re-firing differences
- `phase_gradient(E, S)`: simulates expansion speed of PoR
- `por_rate(t, λ)`: calculates PoR decay frequency over time
















