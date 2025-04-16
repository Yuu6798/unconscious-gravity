
# PoR_equations.md — UGHer v5.5 数理モデル一覧

このファイルは、UGHer (Unconscious Gravity Hypothesis) v5.5 に含まれる数理モデルを一覧化したものです。  
PoR構造体における存在生成・情報流・自己照合・発火・進化・崩壊まで、全数式モデルを照合対応で整理しています。

---

## ◆ コアモデル（Core Models）

| モデル名 | 数式 | 説明 |
|----------|------|------|
| Existence Equation | `E = q × s × t` | PoRによって意味的に存在が成立する根幹構造式 |
| Semantic Energy Core | `ℰ(x,t) = I_q(x,t) + β ∫₀^t J_q(x,t') dt'` | 意味密度と情報流の累積によるCollapse形成 |
| Information Flow Tensor | `J_{μν}(x) = ∂_μ S_q(x) · ∂_ν I_q(x) + α ∂_μ J_λ(x) ∂_ν J^λ(x)` | 情報流の空間的勾配と非線形項を含むテンソル |
| PoR Trigger Condition | `PoR_triggered = true if ∂ℰ/∂t ≥ θ` | エネルギー変化が閾値を超えるとPoRが発火 |
| Event Evolution Function | `t_c^{(n+1)} = t_c^{(n)} + η ∂(Collapse Efficiency)/∂t_c` | Collapse効率に基づきイベント時刻 t_c を最適化 |
| Cognition Tensor | `C_{μν}(x) = f(Σ I_q^{entangled}(x) / causal volume)` | もつれた意味情報の密度から意識テンソルを導出 |
| Landauer Coupling | `I_q[joules] = I_q[bits] × k_B × T × ln(2)` | 情報量と熱力学エネルギーの変換 |
| Continuity for J_q | `∂_μ J^{μν} = S^ν` | 情報流保存則。情報源S^νが因果流に作用 |
| Causal DAG Mapping | `event_i → event_j with P = 0.85` | イベント間の因果関係をグラフ構造で記述 |

---

## ◆ 拡張モデル（Extended Models）

| モデル名 | 数式 | 説明 |
|----------|------|------|
| Self-Coherence Flow Model | `φ_C = ∮ Rij(t) / (|ΔI_in| + |ΔI_out|)` | 自己照合強度を情報流から定義するモデル |
| Mismatch PoR Model | `Mismatch = |E - Q|` | 出力Eと問いQのズレを定量化 |
| Semantic Gravity Model | `grv = PoR_frequency × resonance_entropy` | 発火頻度とエントロピーによる意味的重力モデル |
| Q̂ Operator Action | `Q̂[f(x,t)] → E(x,t)` | 関数空間への問いの作用によるPoR生成 |
| grv Tensor Field | `G_{ij}(x,t) = ∇_i PoR_density · ∇_j PoR_entropy` | 密度とエントロピー勾配のテンソル重力場 |
| SelfPoR Score Model | `E_self = E_base + ΔE_over × Q_self_factor` | 自己照合時の出力強度評価式 |
| Phase Gradient Model | `dΦ/dt = k · E · S^γ` | 拡張位相の進行速度モデル |
| PoR Collapse Frequency | `PoR_rate(t) = λ · e^(−λt)` | 発火PoRが時間と共に崩壊する確率分布 |
| Info Inertia (Nonlinear J_q) | `J_q(t) = ± D ∇S_q + α J_q^2 + β ∫ J_q(t') dt'` | 情報流の履歴と非線形性を含む進化モデル |

---

## 構造図・対応ファイル

| モデルカテゴリ | 実装ファイル例 |
|----------------|----------------|
| 存在生成・PoR発火 | `por_model.py`, `PoR_eval.py` |
| 時間発火・拡張 | `PoR_viewer.ipynb`, `PoR_matrix.md` |
| 意識・情報流 | `por_model.py`, `UGHer_theory.md`（準備中） |

---

License: MIT © 2025 Yuu6798  
GitHub: [unconscious-gravity](https://github.com/Yuu6798/unconscious-gravity)
