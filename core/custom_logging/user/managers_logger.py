from typing import Any
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

USER_CREATE_FILENAME = BASE_DIR / "logs/user/user_create.log"
USER_DELETE_FILENAME = BASE_DIR / "logs/user/user_delete.log"
USER_UPDATE_FILENAME = BASE_DIR / "logs/user/user_update.log"


def initialize_user_managers_logger() -> dict[str, Any]:
    logger = {
        "formatters": {
            "user_formatter": {
                "format": "{levelname} - [{asctime}] [{process}]: {message}",
                "style": "{",
            },
        },
        "handlers": {
            "user_create_file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": USER_CREATE_FILENAME,
                "formatter": "user_formatter",
            },
            "user_delete_file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": USER_DELETE_FILENAME,
                "formatter": "user_formatter",
            },
            "user_update_file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": USER_UPDATE_FILENAME,
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
