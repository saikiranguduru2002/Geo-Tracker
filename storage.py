import json
import os
from datetime import date, timedelta

RESULTS_DIR = "results"

def is_cloud():
    return os.path.exists("/mount/src")

def save_results(brand, category, score, results):
    if is_cloud():
        print("Running on cloud — skipping file save")
        return None

    today = str(date.today())

    data = {
        "date": today,
        "brand": brand,
        "category": category,
        "score": score,
        "results": results
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    filename = os.path.join(RESULTS_DIR, f"{today}.json")

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Results saved to {filename}")
    return filename

def load_yesterday():
    if is_cloud():
        return None

    yesterday = str(date.today() - timedelta(days=1))
    filename = os.path.join(RESULTS_DIR, f"{yesterday}.json")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)

    return None

def load_today():
    if is_cloud():
        return None

    today = str(date.today())
    filename = os.path.join(RESULTS_DIR, f"{today}.json")

    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)

    return None