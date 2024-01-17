import os
from typing import Any
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def initialize_backend_logger() -> dict[str, Any]:
    """Initializes logger for backend.

    This initialization, unlike others, provides `version` and
    `disable_existing_loggers` fields.
    """
    logger = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "main": {
                "format": "{levelname} - [{asctime}] {module} [{process} | {thread}]: {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": os.path.join(BASE_DIR, "logs/django/backend.log"),
                "formatter": "main",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": "INFO",
            },
        },
    }
    return logger
