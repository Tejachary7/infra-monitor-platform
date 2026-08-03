import json
from pathlib import Path


REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def save_metrics(metrics):
    """
    Save the latest monitoring metrics.
    """

    report_file = REPORTS_DIR / "metrics.json"

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )


def save_server_metrics(server_name, metrics):
    """
    Save metrics for one server.
    """

    report_file = REPORTS_DIR / f"{server_name}.json"

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )


def save_all_metrics(metrics_list):
    """
    Save all servers into one report.
    """

    report_file = REPORTS_DIR / "all_servers.json"

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metrics_list,
            file,
            indent=4
        )