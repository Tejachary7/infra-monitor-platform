from logger import logger


def evaluate_services(services):
    """
    Evaluate service health.
    """

    results = {}

    for service, status in services.items():

        healthy = status == "active"

        results[service] = {
            "status": status,
            "healthy": healthy
        }

        if healthy:
            logger.info(f"{service} healthy")
        else:
            logger.warning(f"{service} unhealthy")

    return results