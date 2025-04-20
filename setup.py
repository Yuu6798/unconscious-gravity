# setup.py
from setuptools import setup, find_packages

setup(
    name="unconscious_gravity",
    version="0.1.0",
    description="Monte Carlo simulator and formal models for Point of Resonance (PoR)",
    packages=find_packages(),  # models と metadata パッケージを自動で見つけてくれます
    install_requires=[
        "numpy",
        "pandas",
        "tqdm",
        "transformers",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
    python_requires=">=3.10",
)