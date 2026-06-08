import json
import os
from pathlib import Path


DATA_FILE = Path.home() / ".senior_school.json"


def load_data():
    if not DATA_FILE.exists():
        return {"courses": {}, "enrollments": {}, "payments": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"courses": {}, "enrollments": {}, "payments": {}}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
