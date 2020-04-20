import os

version = os.environ["GITHUB_REF"].split("/")[-1]

with open("turf/version.py", "w") as f:
    f.write(
        f"""\
__version__ = '{str(version)}'\n"""
    )
