from setuptools import setup, find_packages

setup(
    name="weaver",
    version="1.0.0",
    author="Rommelo Yu",
    author_email="developer@discocube.org",
    description="Module to construct a Hamiltonian Cycle in Manhattan Balls in linear time and plot it.",
    packages=find_packages(),
    install_requires=[
        "argparse",
        "numpy",
        "pandas",
        "plotly",
        "pytest",
    ],
    entry_points={"console_scripts": ["weave = main:main"]},
)
