from setuptools import setup, find_packages
setup(
    version="0.1.0",
    description="PoR log diagnostics CLI",
    packages=find_packages(where="src"),   # ← 推奨形
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "tqdm",
        "transformers",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov"
        ]
    },
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "por-diagnose=por_diagnostics.cli:main",
        ],
    },
)
