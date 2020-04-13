import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    version = os.environ["GITHUB_REF"].split("/")[-1]
    print(f"Version: {version}")
except KeyError:
    with open("version.txt") as f:
        __version__ = f.read()
    version = __version__

setup(
    name="pyturf",
    version=version,
    description="Python geospatial library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diogomatoschaves/py-turf",
    author="Diogo Matos Chaves",
    author_email="di.matoschaves@gmail.com",
    packages=[*find_packages(), "turf.utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
