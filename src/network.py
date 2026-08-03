import socket
import requests


def check_ssh(host, port=22, timeout=3):
    """
    Check SSH connectivity.
    """

    try:
        with socket.create_connection(
            (host, port),
            timeout,
        ):
            return True

    except Exception:
        return False


def check_http(host, timeout=5):
    """
    Check HTTP response.
    """

    try:

        response = requests.get(
            f"http://{host}",
            timeout=timeout,
        )

        return response.status_code

    except Exception:

        return None


def check_dns(host):
    """
    Verify DNS/IP resolution.
    """

    try:

        socket.gethostbyname(host)

        return True

    except Exception:

        return False


def scan_port(host, port, timeout=3):
    """
    Scan a single TCP port.
    """

    try:

        with socket.create_connection(
            (host, port),
            timeout,
        ):

            return "OPEN"

    except TimeoutError:

        return "FILTERED"

    except Exception:

        return "CLOSED"


def scan_ports(server, ports):
    """
    Scan multiple ports.
    """

    results = {}

    for port in ports:

        results[port] = scan_port(
            server["host"],
            port,
        )

    return results


def collect_network_metrics(server, config):
    """
    Complete network monitoring.
    """

    return {

        "ssh": check_ssh(
            server["host"],
            server["port"]
        ),

        "http": check_http(
            server["host"]
        ),

        "dns": check_dns(
            server["host"]
        ),

        "ports": scan_ports(
            server,
            config["network_ports"]
        )
    }