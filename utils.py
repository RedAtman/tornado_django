import os
import sqlite3


def create_db(db_file: str = "db.sqlite3"):
    # create the` database file if it doesn't exist
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        conn.close()


def init_db(db_file: str = "db.sqlite3"):
    # create the schema table
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS schema
                    (id integer primary key, name varchar(128), desc varchar(1024))"""
    )
    conn.commit()
    conn.close()

    # insert some data
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO schema (name, desc) VALUES (?, ?)", ("name01", "desc01")
    )
    cursor.execute(
        "INSERT INTO schema (name, desc) VALUES (?, ?)", ("name02", "desc02")
    )
    conn.commit()
    conn.close()


def init_django(settings_module: str = "settings.dev"):

    # Init settings method 1: With settings file(Supports full django project)
    # allow async
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    # # Init settings method 2: Without settings file
    # from pathlib import Path
    # from django.conf import settings
    # BASE_DIR = Path(__file__).resolve().parent
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.sqlite3",
    #         "NAME": BASE_DIR / "db.sqlite3",
    #     }
    # }
    # settings.configure(
    #     **{
    #         "DATABASES": DATABASES,
    #     }
    # )

    from django import VERSION, setup

    if VERSION[:2] > (1, 5):
        setup()
