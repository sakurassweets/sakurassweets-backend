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

# set up logger
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

# Create a console handler and set the level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(levelname)s - [%(asctime)s]: %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

# Output config variables
logger.info("Gunicorn is starting.")
logger.info(f"Gunicorn workers: {workers}")
logger.info(f"Gunicorn bind: {bind}.")
logger.info(f"Gunicorn access log path: {accesslog}.")
logger.info(f"Gunicorn error log path: {errorlog}.")
logger.info("Gunicorn started!")
