#!/usr/bin/env python3
import json
from pathlib import Path

TEMPLATE_HEAD = """[![CI](https://github.com/Yuu6798/unconscious-gravity/actions/workflows/test.yml/badge.svg)](https://github.com/Yuu6798/unconscious-gravity/actions/workflows/test.yml)

# Unconscious Gravity Hypothesis (UGHer)

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
"""

def generate_readme(
    metadata_path: str = "metadata/semantic_index.json",
    output_path: str = "README.generated.md"
):
    # メタデータ読み込み
    with open(metadata_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 自動生成部の開始マーカー＋ヘッダ
    sections = ["<!-- BEGIN_AUTO_README -->", TEMPLATE_HEAD]

    # 各セクションを組み立て
    for name, entry in data.items():
        sections.append(
            TEMPLATE_ENTRY.format(
                name=name,
                formula=entry.get("formula", ""),
                description=entry.get("description", ""),
                tags=", ".join(entry.get("tags", []))
            )
        )

    # フェーズ2 Quick‑start と Footer、終了マーカー
    sections.extend([TEMPLATE_PHASE2, TEMPLATE_FOOTER, "<!-- END_AUTO_README -->"])

    # ファイル出力
    result = "\n".join(sections)
    Path(output_path).write_text(result, encoding="utf-8")
    print(f"README generated at {output_path}")

if __name__ == "__main__":
    generate_readme()