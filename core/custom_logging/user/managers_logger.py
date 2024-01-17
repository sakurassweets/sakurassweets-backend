import os
from typing import Any
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def initialize_user_managers_logger() -> dict[str, Any]:
    logger = {
        "formatters": {
            "user_formatter": {
                "format": "{levelname} - [{asctime}] [{process} | {thread}] {message}",
                "style": "{",
            },
        },
        "handlers": {
            "user_create_file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/user/user_create.log"),
                "formatter": "user_formatter",
            },
            "user_delete_file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/user/user_delete.log"),
                "formatter": "user_formatter",
            },
            "user_update_file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/user/user_update.log"),
                "formatter": "user_formatter",
            }
        },
        "loggers": {
            "user_create": {
                "handlers": ["user_create_file"],
                "level": "INFO",
            },
            "user_delete": {
                "handlers": ["user_delete_file"],
                "level": "INFO",
            },
            "user_update": {
                "handlers": ["user_update_file"],
                "level": "INFO",
            }
        },
    }
    return logger
