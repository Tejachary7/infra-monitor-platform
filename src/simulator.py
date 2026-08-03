from logger import logger


def stop_service(ssh, service):
    """
    Stop a service intentionally.
    """

    output, error = ssh.execute(
        f"sudo systemctl stop {service}"
    )

    if error:
        logger.error(f"Failed to stop {service}")
        return False

    logger.warning(f"{service} intentionally stopped")

    return True


def start_service(ssh, service):
    """
    Start a service manually.
    """

    output, error = ssh.execute(
        f"sudo systemctl start {service}"
    )

    if error:
        logger.error(f"Failed to start {service}")
        return False

    logger.info(f"{service} started")

    return True