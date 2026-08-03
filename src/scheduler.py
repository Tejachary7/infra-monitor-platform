import time
from datetime import datetime

from logger import logger
from main import main


def scheduler(interval=300):
    """
    Run monitoring every 'interval' seconds.
    """

    logger.info("Scheduler Started")

    while True:

        print("\n" + "=" * 80)
        print(f"Monitoring Cycle : {datetime.now()}")
        print("=" * 80)

        try:
            main()

        except Exception as e:
            logger.exception(e)

        print(f"\nSleeping for {interval} seconds...\n")

        time.sleep(interval)


if __name__ == "__main__":
    scheduler()