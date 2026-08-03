import time
from concurrent.futures import ThreadPoolExecutor

from banner import show_banner

from inventory import load_inventory
from config_loader import load_config
from ssh import SSHClient
from logger import logger

from monitor import collect_metrics
from network import collect_network_metrics

from recovery import recover_services
from alerts import generate_alerts

from log_analysis import (
    analyze_logs,
    save_log_report
)

from reports import save_metrics

from history import save_history

from incident import generate_incident_report


def monitor_server(server, config):

    logger.info(
        f"Monitoring started for {server['name']}"
    )

    print("\n" + "=" * 80)
    print(
        f"Server : {server['name']} ({server['host']})"
    )
    print("=" * 80)

    ssh = SSHClient(
        host=server["host"],
        username=server["username"],
        port=server["port"],
        key_file=server["key_file"],
    )

    if not ssh.connect():

        logger.error(
            f"Connection failed : {server['name']}"
        )

        print("❌ Connection Failed")

        return None

    print("✅ Connected")

    # =====================================
    # Monitoring
    # =====================================

    metrics = collect_metrics(
        ssh,
        config
    )

    metrics["network"] = collect_network_metrics(
        server,
        config
    )

    metrics["server"] = {

        "name": server["name"],

        "host": server["host"]

    }

    # =====================================
    # Recovery
    # =====================================

    recovery = recover_services(
        ssh,
        metrics["services"]
    )

    metrics["recovery"] = recovery

    # =====================================
    # Alerts
    # =====================================

    generate_alerts(
        metrics,
        config
    )

    # =====================================
    # Log Analysis
    # =====================================

    logs = analyze_logs(ssh)

    metrics["logs"] = logs

    save_log_report(
        server["name"],
        logs
    )

    # =====================================
    # Reports
    # =====================================

    save_metrics(metrics)

    save_history(metrics)

    generate_incident_report(metrics)

    # =====================================
    # Display
    # =====================================

    print("\nCPU")
    print("-" * 50)

    cpu = metrics["resources"]["cpu"]

    print(f"Usage : {cpu}%")

    if cpu >= config["cpu_threshold"]:
        print("Status : ⚠ HIGH CPU")
    else:
        print("Status : ✅ HEALTHY")

    # -------------------------------------

    memory = metrics["resources"]["memory"]

    print("\nMemory")
    print("-" * 50)

    print(f"Total : {memory['total_mb']} MB")
    print(f"Used  : {memory['used_mb']} MB")
    print(f"Free  : {memory['free_mb']} MB")
    print(f"Usage : {memory['usage_percent']}%")

    if memory["usage_percent"] >= config["memory_threshold"]:
        print("Status : ⚠ HIGH MEMORY")
    else:
        print("Status : ✅ HEALTHY")

    # -------------------------------------

    disk = metrics["resources"]["disk"]

    print("\nDisk")
    print("-" * 50)

    print(f"Filesystem : {disk['filesystem']}")
    print(f"Size       : {disk['size']}")
    print(f"Used       : {disk['used']}")
    print(f"Available  : {disk['available']}")
    print(f"Usage      : {disk['usage_percent']}%")

    if disk["usage_percent"] >= config["disk_threshold"]:
        print("Status : ⚠ HIGH DISK")
    else:
        print("Status : ✅ HEALTHY")

    # -------------------------------------

    print("\nServices")
    print("-" * 50)

    for service, info in metrics["services"].items():

        icon = "✅" if info["healthy"] else "❌"

        print(
            f"{service:<15}: "
            f"{info['status']:<10} "
            f"{icon}"
        )

    # -------------------------------------

    print("\nRecovery")
    print("-" * 50)

    for service, result in recovery.items():

        if result["action"] == "None":

            print(
                f"{service:<15}: Healthy"
            )

        else:

            status = (
                "SUCCESS"
                if result["success"]
                else "FAILED"
            )

            print(
                f"{service:<15}: "
                f"{result['action']} -> {status}"
            )

    # -------------------------------------

    system = metrics["system"]

    print("\nSystem")
    print("-" * 50)

    print(f"Hostname      : {system['hostname']}")
    print(f"OS            : {system['os']}")
    print(f"Kernel        : {system['kernel']}")
    print(f"Architecture  : {system['architecture']}")
    print(f"Uptime        : {system['uptime']}")
    print(f"Load Average  : {system['load_average']}")

    # -------------------------------------

    network = metrics["network"]

    print("\nNetwork")
    print("-" * 50)

    print(
        f"SSH  : {'ONLINE' if network['ssh'] else 'OFFLINE'}"
    )

    if network["http"] is None:
        print("HTTP : OFFLINE")
    else:
        print(f"HTTP : {network['http']}")

    print(
        f"DNS  : {'OK' if network['dns'] else 'FAILED'}"
    )

    print("\nPort Scan")
    print("-" * 50)

    for port, status in network["ports"].items():

        print(f"{port:<5}: {status}")

    ssh.disconnect()

    logger.info(
        f"Monitoring completed for {server['name']}"
    )

    return metrics

from dashboard import generate_dashboard
from report_generator import generate_summary_report


def main():

    logger.info("=" * 80)
    logger.info("Infrastructure Monitoring Started")

    servers = load_inventory()
    config = load_config()

    show_banner(
    len(servers),
    config
               )
    start = time.time()

    all_metrics = []

    with ThreadPoolExecutor(
        max_workers=len(servers)
    ) as executor:

        futures = [

            executor.submit(
                monitor_server,
                server,
                config
            )

            for server in servers

        ]

        for future in futures:

            result = future.result()

            if result:

                all_metrics.append(result)

    # =====================================
    # Dashboard
    # =====================================

    generate_dashboard(
        all_metrics
    )

    # =====================================
    # Reports
    # =====================================

    generate_summary_report(
        all_metrics,
        "daily"
    )

    # Uncomment these when implementing
    # automatic scheduling.
    #
    # generate_summary_report(
    #     all_metrics,
    #     "weekly"
    # )
    #
    # generate_summary_report(
    #     all_metrics,
    #     "monthly"
    # )

    end = time.time()

    logger.info(
        f"Execution Time : {end-start:.2f} seconds"
    )

    logger.info(
        "Monitoring Finished"
    )

    print("\n" + "=" * 80)

    print(
        "Monitoring Completed Successfully"
    )

    print(
        f"Servers Checked : {len(all_metrics)}"
    )

    print(
        f"Execution Time : {end-start:.2f} seconds"
    )

    print(
        "\nGenerated Files"
    )

    print("-" * 80)

    print("✓ dashboard/dashboard.html")

    print("✓ reports/metrics.json")

    print("✓ reports/incident_report.html")

    print("✓ reports/log_report.json")

    print("✓ reports/history_server*.json")

    print("✓ reports/daily/")

    print("=" * 80)


if __name__ == "__main__":
    main()