from logger import logger


def restart_service(ssh, service):
    """
    Restart a systemd service.
    """

    command = f"sudo systemctl restart {service}"

    _, error = ssh.execute(command)

    if error:
        logger.error(f"{service} restart failed")
        return False

    logger.info(f"{service} restart command executed")

    return True


def verify_service(ssh, service):
    """
    Verify service state after recovery.
    """

    output, error = ssh.execute(
        f"systemctl is-active {service}"
    )

    if error:
        return False

    return output.strip() == "active"


def recover_services(ssh, services):
    """
    Recover unhealthy services and update their status.
    """

    results = {}

    for service, info in services.items():

        # Already healthy
        if info["healthy"]:

            results[service] = {
                "action": "None",
                "success": True
            }

            continue

        # Restart service
        restarted = restart_service(
            ssh,
            service
        )

        verified = False

        if restarted:
            verified = verify_service(
                ssh,
                service
            )

        # Update the service dictionary if recovery succeeded
        if verified:
            info["status"] = "active"
            info["healthy"] = True

        results[service] = {
            "action": "Restart",
            "success": verified
        }

    return results