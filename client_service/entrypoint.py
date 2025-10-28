import os
import sys
import time

from django.core.management import execute_from_command_line
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "client_service.settings")


def wait_for_db(retries=10, delay=3):
    for i in range(retries):
        try:
            connection = connections["default"]
            connection.ensure_connection()
            return
        except OperationalError:
            time.sleep(delay)
    sys.exit(1)


if __name__ == "__main__":
    wait_for_db()
    execute_from_command_line(["manage.py", "migrate", "--noinput"])
    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8001"])
