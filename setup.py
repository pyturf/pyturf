import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    __version__ = os.environ["GITHUB_REF"].split("/")[-1].strip('"')
    print(f"Version: {__version__}")
except KeyError:
    try:
        from turf.version import __version__
    except ModuleNotFoundError:
        __version__ = str(
            open("turf/version.py").read().split(" ")[-1].splitlines()[0]
        ).strip('"')

setup(
    name="pyturf",
    version=__version__,
    description="Python geospatial library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyturf/pyturf",
    author="Diogo Matos Chaves, Steffen Häußler",
    author_email="di.matoschaves@gmail.com",
    packages=[*find_packages(), "turf.utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=["rtree"],
    test_requires=["pytest", "pytest-cov"],
)
