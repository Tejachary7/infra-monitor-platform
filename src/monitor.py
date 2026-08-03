import re
from datetime import datetime

from services import evaluate_services


def get_cpu_usage(ssh):
    """
    Get CPU usage percentage.
    """

    output, error = ssh.execute(
        "top -bn1 | grep '%Cpu'"
    )

    if error:
        return None

    match = re.search(
        r"(\d+\.\d+)\s+id",
        output,
    )

    if not match:
        return None

    idle = float(match.group(1))

    return round(100 - idle, 2)


def get_memory_usage(ssh):
    """
    Get memory usage.
    """

    output, error = ssh.execute(
        "free -m"
    )

    if error:
        return None

    lines = output.splitlines()

    mem = lines[1].split()

    total = int(mem[1])
    used = int(mem[2])
    free = int(mem[3])

    return {
        "total_mb": total,
        "used_mb": used,
        "free_mb": free,
        "usage_percent": round(
            used / total * 100,
            2
        )
    }


def get_disk_usage(ssh):
    """
    Get root filesystem usage.
    """

    output, error = ssh.execute(
        "df -h /"
    )

    if error:
        return None

    lines = output.splitlines()

    disk = lines[1].split()

    return {
        "filesystem": disk[0],
        "size": disk[1],
        "used": disk[2],
        "available": disk[3],
        "usage_percent": int(
            disk[4].replace("%", "")
        ),
        "mount": disk[5]
    }


def get_service_status(ssh, services):
    """
    Get status of monitored services.
    """

    results = {}

    for service in services:

        output, error = ssh.execute(
            f"systemctl is-active {service}"
        )

        if error:
            results[service] = "ERROR"
        else:
            results[service] = output.strip()

    return results


def get_system_information(ssh):
    """
    Collect general system information.
    """

    system = {}

    commands = {

        "hostname":
            "hostname",

        "os":
            "grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"'",

        "kernel":
            "uname -r",

        "architecture":
            "uname -m",

        "uptime":
            "uptime -p",

        "load_average":
            "cat /proc/loadavg"

    }

    for key, command in commands.items():

        output, error = ssh.execute(command)

        if error:
            system[key] = "UNKNOWN"
        else:
            system[key] = output.strip()

    return system


def collect_metrics(ssh, config):
    """
    Complete monitoring engine.
    """

    raw_services = get_service_status(
        ssh,
        config["services"]
    )

    service_health = evaluate_services(
        raw_services
    )

    return {

        "timestamp":
            datetime.now().isoformat(),

        "system":
            get_system_information(ssh),

        "resources": {

            "cpu":
                get_cpu_usage(ssh),

            "memory":
                get_memory_usage(ssh),

            "disk":
                get_disk_usage(ssh),

        },

        "services":
            service_health
    }