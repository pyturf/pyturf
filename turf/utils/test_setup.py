import json
import os
from collections import defaultdict


def get_fixtures(current_path, fixtures=None, keys=None):

    if not fixtures:
        fixtures = defaultdict(lambda: {"in": None, "out": None})

    if not keys:
        keys = ["in", "out"]

    for key in keys:

        files_path = os.path.join(current_path, key)

        for filename in os.listdir(files_path):
            with open(os.path.join(files_path, filename), "r") as f:
                name = ".".join(filename.split(".")[:-1])
                fixtures[name][key] = json.load(f)

    return fixtures
