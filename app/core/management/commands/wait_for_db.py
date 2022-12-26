# Django command to make db wait andf available
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")

        db_up = False
        n = 1
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                message = "Database loading" + "." * n
                n += 1
                self.stdout.write(self.style.ERROR(message))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database Available"))
