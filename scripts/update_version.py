import os

version = os.environ["GITHUB_REF"].split("/")[-1]

with open("version.txt", "w") as f:
    f.write(str(version))
