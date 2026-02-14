import json
import os

def load_schemes():
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "data", "schemes.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)