import json
import os
from datetime import date, timedelta

RESULTS_DIR = "results"

def save_results(brand, category, score, results):
    today = str(date.today())

    data = {
        "date": today,
        "brand": brand,
        "category": category,
        "score": score,
        "results": results
    }

    filename = os.path.join(RESULTS_DIR, f"{today}.json")

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Results saved to {filename}")
    return filename

def load_yesterday():
    yesterday = str(date.today() - timedelta(days=1))
    filename = os.path.join(RESULTS_DIR, f"{yesterday}.json")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)

    return None

def load_today():
    today = str(date.today())
    filename = os.path.join(RESULTS_DIR, f"{today}.json")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)

    return None