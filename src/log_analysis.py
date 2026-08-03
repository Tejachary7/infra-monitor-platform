import json
from pathlib import Path


REPORT = Path("reports/log_report.json")


def analyze_logs(ssh):

    report = {}

    commands = {

        "failed_logins":
        "journalctl -n 200 | grep 'Failed password' | tail -10",

        "successful_logins":
        "journalctl -n 200 | grep 'Accepted password\\|Accepted publickey' | tail -10",

        "nginx_logs":
        "journalctl -u nginx -n 20",

        "ssh_logs":
        "journalctl -u ssh -n 20",

        "system_errors":
        "journalctl -p err -n 20"

    }

    for name, command in commands.items():

        output, error = ssh.execute(command)

        if error:
            report[name] = []
        else:
            report[name] = output.splitlines()

    return report


def save_log_report(server, report):

    REPORT.parent.mkdir(exist_ok=True)

    with open(REPORT, "w", encoding="utf-8") as file:

        json.dump(
            {
                "server": server,
                "logs": report
            },
            file,
            indent=4
        )