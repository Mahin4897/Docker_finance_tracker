import time
from django.db import connections
from django.db.utils import OperationalError

db_conn = None
while not db_conn:
    try:
        db_conn = connections["default"]
        db_conn.cursor()
    except OperationalError:
        print("Waiting for database...")
        time.sleep(2)

print("Database available!")
