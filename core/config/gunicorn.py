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

accesslog = os.path.join(logs_path, "gunicorn_access.log")
if not os.path.exists(accesslog):
    with open(accesslog, 'w'):
        pass
    print(f"The file at {accesslog} did not exist and has been created.")

errorlog = os.path.join(logs_path, "gunicorn_error.log")
if not os.path.exists(errorlog):
    with open(errorlog, 'w'):
        pass
    print(f"The file at {errorlog} did not exist and has been created.")

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
