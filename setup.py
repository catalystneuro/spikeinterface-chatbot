from pathlib import Path

from setuptools import setup, find_packages

root = Path(__file__).parent

with open(root / "requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="spikeinterface-chatbot",
    version="0.0.3",
    description="A chatbot for spikeinterface",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
)
