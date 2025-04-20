from setuptools import setup, find_packages

setup(
    name="unconscious_gravity",
    version="0.1.0",
    packages=find_packages(include=["models", "metadata"]),
    install_requires=[
        "numpy",
        "pandas",
        "tqdm",
        "transformers",
    ],
    extras_require={
        "test": ["pytest"],
    },
)