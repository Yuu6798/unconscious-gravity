from setuptools 
import setup, find_packages

setup(
    name="unconscious_gravity_exp",
    version="0.0.9",
    description="PoR log diagnostics CLI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "tqdm",
        "transformers",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "por-diagnose=ugher_exp.por_detector:main",
        ],
    },
)