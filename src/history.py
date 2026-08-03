import json
from pathlib import Path

HISTORY_FILE = Path("reports/history.json")


def save_history(metrics):

    HISTORY_FILE.parent.mkdir(exist_ok=True)

    if HISTORY_FILE.exists():

        with open(HISTORY_FILE, "r", encoding="utf-8") as file:

            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = []

    else:

        history = []

    history.append(metrics)

    history = history[-100:]

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:

        json.dump(
            history,
            file,
            indent=4
        )


def history_summary(history):

    cpu = [
        item["resources"]["cpu"]
        for item in history
    ]

    memory = [
        item["resources"]["memory"]["usage_percent"]
        for item in history
    ]

    return {

        "checks": len(history),

        "max_cpu": max(cpu),

        "average_cpu": round(
            sum(cpu) / len(cpu),
            2
        ),

        "average_memory": round(
            sum(memory) / len(memory),
            2
        )

    }