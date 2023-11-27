import multiprocessing
import os
import logging
from dotenv import load_dotenv


load_dotenv()

# Assuming gunicorn.py is in the core folder
core_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(core_path)

# Workers configuration
bind = os.getenv("WEB_BIND", "0.0.0.0:8000")
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 30
graceful_timeout = 30

# Logging
logs_path = os.path.join(project_path, "logs")
os.makedirs(logs_path, exist_ok=True)  # Ensure the "logs" directory exists


def create_file_if_does_not_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
        print(f"The file at {file_path} did not exist and has been created.")


accesslog = os.path.join(logs_path, "gunicorn_access.log")
create_file_if_does_not_exists(accesslog)

errorlog = os.path.join(logs_path, "gunicorn_error.log")
create_file_if_does_not_exists(errorlog)


loglevel = "info"

# Whether to send Django output to the error log
capture_output = True

# Output config variables
logging.info("Gunicorn is starting.")
logging.info(f"Gunicorn workers: {workers}")
logging.info(f"Gunicorn bing: {bind}.")
logging.info(f"Gunicorn access log path: {accesslog}.")
logging.info(f"Gunicorn error log path: {errorlog}.")
logging.info("Gunicorn started!")
