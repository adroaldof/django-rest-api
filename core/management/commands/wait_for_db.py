import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("\nTrying to connect to the database"))
        database_connection = None

        while not database_connection:
            try:
                database_connection = connections["default"]
            except OperationalError:
                self.stdout.write("Waiting for the database...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database is available"))
