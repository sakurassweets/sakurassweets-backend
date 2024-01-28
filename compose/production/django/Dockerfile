# define an alias for the specific python version used in this file.
FROM python:3.12-slim-bookworm as python

# Python build stage
FROM python as python-build-stage

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
    -r requirements.txt


# Python 'run' stage
FROM python as python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

RUN addgroup --system debian && adduser --system --group debian


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    # psycopg2 dependencies
    libpq-dev \
    # Translations dependencies
    gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# Install linting tools
RUN pip install --upgrade pip
RUN pip install flake8

# Create logfiles
RUN mkdir -p /app/core/logs/django && chown -R debian:debian /app/core && touch /app/core/logs/django/backend.log
RUN mkdir -p /app/core/logs/user 
RUN touch /app/core/logs/user/user_create.log
RUN touch /app/core/logs/user/user_delete.log
RUN touch /app/core/logs/user/user_update.log

# Grant write permissions to the user 'django'
RUN chmod 775 /app/core/logs/django/
RUN chmod 775 /app/core/logs/django/backend.log
RUN chmod 775 /app/core/logs/user/user_create.log
RUN chmod 775 /app/core/logs/user/user_delete.log
RUN chmod 775 /app/core/logs/user/user_update.log


COPY --chown=debian:debian ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=debian:debian ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY --chown=debian:debian ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

RUN flake8 --ignore=E501,F401 .

# copy application code to WORKDIR
COPY --chown=debian:debian . ${APP_HOME}

# make django owner of the WORKDIR directory as well.
RUN chown -R debian:debian ${APP_HOME}

USER debian

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

ENTRYPOINT ["/entrypoint"]