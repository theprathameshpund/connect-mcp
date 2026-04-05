import os
import json


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)