import json
import os

SAVE_FILE = "highscore.json"

def load_high_score():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                return data.get("highscore", 0)
        except:
            return 0
    return 0

def save_high_score(score):
    with open(SAVE_FILE, "w") as f:
        json.dump({"highscore": score}, f)
