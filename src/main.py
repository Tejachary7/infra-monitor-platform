import time
from concurrent.futures import ThreadPoolExecutor

from inventory import load_inventory
from config_loader import load_config
from ssh import SSHClient
from logger import logger


# Base monitoring commands
BASE_COMMANDS = [
    "hostname",
    "uptime",
    "free -h",
    "df -h",
    "nproc",
    "uname -r",
    "ip -4 addr show",
]


def monitor_server(server, config):
    """
    Monitor one server.
    """

    logger.info(f"Monitoring started for {server['name']}")

    print("\n" + "=" * 80)
    print(f"Server : {server['name']} ({server['host']})")
    print("=" * 80)

    ssh = SSHClient(
        host=server["host"],
        username=server["username"],
        port=server["port"],
        key_file=server["key_file"],
    )

    if not ssh.connect():
        logger.error(f"Connection failed: {server['name']}")
        print("❌ Connection Failed")
        return

    print("✅ Connected")

    # Run base commands
    for command in BASE_COMMANDS:

        print(f"\n$ {command}")

        output, error = ssh.execute(command)

        if error:
            logger.error(f"{server['name']} | {command} | {error}")
            print(error)
        else:
            logger.info(f"{server['name']} | {command} | SUCCESS")
            print(output)

    # Run service checks from config.yaml
    print("\nService Status")
    print("-" * 80)

    for service in config["services"]:

        command = f"systemctl is-active {service}"

        output, error = ssh.execute(command)

        if error:
            logger.error(f"{server['name']} | {service} | {error}")
            print(f"{service:<15}: ERROR")
        else:
            logger.info(f"{server['name']} | {service} | {output}")
            print(f"{service:<15}: {output}")

    ssh.disconnect()

    logger.info(f"Monitoring completed for {server['name']}")


def main():

    logger.info("=" * 80)
    logger.info("Infrastructure Monitoring Started")

    servers = load_inventory()
    config = load_config()

    print("=" * 80)
    print("Infrastructure Monitoring Platform")
    print("=" * 80)

    print(f"\nLoaded Servers : {len(servers)}")

    print("\nConfiguration")
    print("-" * 80)

    print(f"CPU Threshold     : {config['cpu_threshold']}%")
    print(f"Memory Threshold  : {config['memory_threshold']}%")
    print(f"Disk Threshold    : {config['disk_threshold']}%")
    print(f"Check Interval    : {config['check_interval']} seconds")

    print("\nServices To Monitor")

    for service in config["services"]:
        print(f" • {service}")

    print("\nPorts To Monitor")

    for port in config["network_ports"]:
        print(f" • {port}")

    start = time.time()

    with ThreadPoolExecutor(max_workers=len(servers)) as executor:

        futures = []

        for server in servers:
            futures.append(
                executor.submit(
                    monitor_server,
                    server,
                    config
                )
            )

        for future in futures:
            future.result()

    end = time.time()

    logger.info(f"Execution Time : {end-start:.2f} seconds")
    logger.info("Infrastructure Monitoring Finished")
    logger.info("=" * 80)

    print("\n" + "=" * 80)
    print("Monitoring Finished Successfully")
    print(f"Execution Time : {end-start:.2f} seconds")
    print("=" * 80)


if __name__ == "__main__":
    main()