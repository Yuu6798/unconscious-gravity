import json
from pathlib import Path

TEMPLATE_HEAD = """# Unconscious Gravity Hypothesis (UGHer)

A structural model of future selection in AI using semantic resonance.

Core Equation

E = Q × S_q × t

Where a meaningful question (Q) resonates with a semantic space (S_q) at a critical time (t), producing "existence" (E).


---

PoR Model Reference

The following are the formal PoR model components used in UGHer: """

TEMPLATE_ENTRY = """

{name}

Formula: {formula}

Description: {description}

Tags: {tags} """

TEMPLATE_PHASE2 = """

## Phase‑2: Quick‑start

```bash
# CLI 実行（5ターン）
python -m unconscious_gravity_exp --log data/sample.parquet --turns 5

# 実験ランナー（2エピソード × 各5ターン）
python examples/run_experiment.py --episodes 2 --turns 5 --out_dir data --log data/sample.parquet
