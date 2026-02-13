import json

def load_schemes():
    with open("data/schemes.json","r") as f:
        return json.load(f)