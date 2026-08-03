from pathlib import Path
from datetime import datetime

ALERT_FILE = Path("logs/alerts.log")


def write_alert(server, level, message):

    ALERT_FILE.parent.mkdir(exist_ok=True)

    with open(ALERT_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file.write(
            f"[{timestamp}] "
            f"[{level}] "
            f"[{server}] "
            f"{message}\n"
        )


def generate_alerts(metrics, config):

    server = metrics["server"]["name"]

    # CPU

    cpu = metrics["resources"]["cpu"]

    if cpu >= config["cpu_threshold"]:

        write_alert(
            server,
            "WARNING",
            f"CPU Usage High ({cpu}%)"
        )

    # Memory

    memory = metrics["resources"]["memory"]["usage_percent"]

    if memory >= config["memory_threshold"]:

        write_alert(
            server,
            "WARNING",
            f"Memory Usage High ({memory}%)"
        )

    # Disk

    disk = metrics["resources"]["disk"]["usage_percent"]

    if disk >= config["disk_threshold"]:

        write_alert(
            server,
            "WARNING",
            f"Disk Usage High ({disk}%)"
        )

    # Services

    for service, info in metrics["services"].items():

        if not info["healthy"]:

            write_alert(
                server,
                "CRITICAL",
                f"{service} service is {info['status']}"
            )

    # Recovery

    if "recovery" in metrics:

        for service, recovery in metrics["recovery"].items():

            if not recovery["success"]:

                write_alert(
                    server,
                    "CRITICAL",
                    f"{service} recovery failed"
                )