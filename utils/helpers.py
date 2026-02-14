import json

def load_schemes():
    with open("data/schemes.json", "r", encoding="utf-8") as f:
        return json.load(f)