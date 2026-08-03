from pathlib import Path
import paramiko

from logger import logger


class SSHClient:

    def __init__(self, host, username, port=22, key_file=None):
        self.host = host
        self.username = username
        self.port = port
        self.key_file = key_file
        self.client = None

    def connect(self):

        try:

            self.client = paramiko.SSHClient()

            self.client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )

            self.client.connect(
                hostname=self.host,
                username=self.username,
                port=self.port,
                key_filename=str(Path(self.key_file).expanduser()),
                timeout=10
            )

            logger.info(f"Connected to {self.host}")

            return True

        except Exception as e:

            logger.error(f"{self.host} : {e}")

            return False

    def execute(self, command):

        stdin, stdout, stderr = self.client.exec_command(command)

        output = stdout.read().decode().strip()

        error = stderr.read().decode().strip()

        logger.info(f"{self.host} -> {command}")

        return output, error

    def disconnect(self):

        if self.client:
            self.client.close()
            logger.info(f"Disconnected from {self.host}")