import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def initialize_db_logger():
    logger = {
        "formatters": {
            "main": {
                "format": "{levelname} - [{asctime}] [{process} | {thread}]: {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/django/db.log"),
                "formatter": "main",
            },
        },
        "loggers": {
            "django.db.connection": {
                "handlers": ["file"],
                "level": "DEBUG",
            },
        },
    }
    return logger
