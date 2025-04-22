# scripts/generate_readme.py

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

TEMPLATE_FOOTER = """

Generated from metadata/semantic_index.json
"""

def generate_readme(metadata_path: str = "metadata/semantic_index.json", output_path: str = "README.generated.md"):
    with open(metadata_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sections = [TEMPLATE_HEAD]
    for name, entry in data.items():
        formula = entry.get("formula", "")
        description = entry.get("description", "")
        tags = ", ".join(entry.get("tags", []))
        sections.append(TEMPLATE_ENTRY.format(
            name=name,
            formula=formula,
            description=description,
            tags=tags
        ))
    sections.append(TEMPLATE_FOOTER)

    result = "\n".join(sections)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"README generated at {output_path}")

if __name__ == "__main__":
    generate_readme()