#!/usr/bin/env python3
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
```"""
TEMPLATE_FOOTER = """

Generated from metadata/semantic_index.json
"""

def generate_readme(
    metadata_path: str = "metadata/semantic_index.json",
    output_path: str = "README.generated.md"
):
    # メタデータ読み込み
    with open(metadata_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 自動生成部の開始マーカー
    sections = ["<!-- BEGIN_AUTO_README -->", TEMPLATE_HEAD]

    # 各セクションを組み立て
    for name, entry in data.items():
        formula     = entry.get("formula", "")
        description = entry.get("description", "")
        tags        = ", ".join(entry.get("tags", []))
        sections.append(
            TEMPLATE_ENTRY.format(
                name=name,
                formula=formula,
                description=description,
                tags=tags
            )
        )

    # フェーズ2 Quick‑start とフッターを追加
    sections.append(TEMPLATE_PHASE2)
    sections.append(TEMPLATE_FOOTER)

    # 自動生成部の終了マーカー
    sections.append("<!-- END_AUTO_README -->")

    # ファイル出力
    result = "\n".join(sections)
    Path(output_path).write_text(result, encoding="utf-8")
    print(f"README generated at {output_path}")

if __name__ == "__main__":
    generate_readme()