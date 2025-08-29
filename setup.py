from setuptools import setup, find_packages

setup(
    name="art-tactile-transform",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "Pillow",
        "requests",
        "pytest",
    ],
    python_requires=">=3.10",
)