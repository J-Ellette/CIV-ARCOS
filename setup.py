"""Setup configuration for CIV-ARCOS."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="civ-arcos",
    version="0.1.0",
    author="CIV-ARCOS Project",
    description="Civilian Assurance-based Risk Computation and Orchestration System - Military-grade assurance for civilian code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/J-Ellette/CIV-ARCOS",
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "civ-arcos=civ_arcos.api:main",
        ],
    },
)
