import json
import os

def get_config():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json'), encoding="utf-8") as f:
        return json.load(f)

def update_config(new_config):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json'), 'w', encoding="utf-8") as f:
        json.dump(new_config, f, indent=4)