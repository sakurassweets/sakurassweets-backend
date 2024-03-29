# Sakuras Sweets

<h3>Welcome to the Sakuras Sweets! Below are instructions on setting up and running the project API locally</h3>

## Technology stack used

### Build with:

<img src="https://img.shields.io/badge/Python-244c6f?logo=python&logoColor=white&style=ShieldStyle"> <img src="https://img.shields.io/badge/Django-0c4b33?logo=django&logoColor=white&style=ShieldStyle" />
<img src="https://img.shields.io/badge/Django%20Rest%20Framework-a30000?logo=django&logoColor=white&style=ShieldStyle" /> <img src="https://img.shields.io/badge/Docker-ffffff?logo=docker&logoColor=White&style=ShieldStyle" />

### Version Control and Development Tools used:

<img src="https://img.shields.io/badge/Git-DC4936?logo=git&logoColor=white&style=ShieldStyle" /> <img src="https://img.shields.io/badge/GitHub-1A1C1E?logo=github&logoColor=white&style=ShieldStyle" /> <img src="https://img.shields.io/badge/Visual Studio Code-0C72C5?logo=visual studio code&logoColor=white&style=ShieldStyle" />

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) (v3.12.0 or later)
- [PostgreSQL](https://www.postgresql.org/) (v16 or later)
- [Redis](https://redis.io/) (v7.2.3 or later)

> all other dependensies will be installed via `requirements.txt`

### API Documentation:

- [Documentation](https://github.com/sakurassweets/sakurassweets-backend/tree/main/docs)

## Deployment with Docker and Docker Compose

**Clone the repository:**

```bash
$ git clone https://github.com/sakurassweets/sakurassweets-backend
```

**Enter project folder:**

```bash
$ cd sakurassweets-backend
```

**Setup the .env file (check next topic)**

**Build & Run project**

```bash
$ docker compose -f local.yml up -d --build
```

**Go to: [http://localhost:80](http://localhost:80)**

### Using Docker you can create DB backups

You can use commands only when container runs

**Create backup:**

```bash
$ docker compose -f local.yml exec db backup
```

**List backups:**

```bash
$ docker compose -f local.yml exec db backups
```

**Restore DB from backup:**

<1> - Filename of an existing backup.

```bash
$ docker compose -f local.yml exec db restore <1>
```

**Remove backup:**

<1> - Filename of a backup to remove.

```bash
$ docker-compose -f local.yml exec db rmbackup <1>
```

# The .env setup

Note: "0.0.0.0" as host means any IP used with provided port.

## DB setup (if using PosgreSQL):

- Find the `.env.example` file in project
- Rename it to `.env` and open
- Set _`DB_NAME`_, _`DB_USER`_, _`DB_PASS`_, to whatever you want.
- Set _`DB_HOST`_ to `db` for non production deployment.
- Set _`DB_PORT`_ to `5432` (default for PostgreSQL).
- Set _`DB_ENGINE`_ to you'r backend for DB. Default is `"django.db.backends.postgresql"` for PostgreSQL.

## Other variables:

**Django variables:**

- `DJANGO_SECRET_KEY`: Randomly generated secret key by default but recommended to add your own key (just generate it and paste in). Used in JWT generation.
- `DJANGO_ALLOWED_HOSTS`: Hosts that can actually host project. Just set it to: `localhost, 127.0.0.1, 0.0.0.0` for non production deployment.
- `DEBUG`: Django debug mode. If something goes wrong django shows you debug message with problem. Set `1` to set it as `True`, and `0` for `False`
- `CSRF_TRUSTED`: Trusted origins for CSRF operations. For example sending some data through POST request from input form on website. Set it to: `http://localhost, http://127.0.0.1, http://0.0.0.0` for non production deployment.
- `CORS_ORIGINS`: Origins that allowed to make requests through CORS validation. Set it to same as `CSRF_TRUSTED`.

**Email sending variables:**

Note: To use email sending read [this](https://reintech.io/blog/setting-up-email-in-django-tutorial), if you don't want to do this just set _`SEND_EMAIL`_ to `False`.

- `EMAIL_HOST`: In most cases the email from which emails will be sended to user.
- `EMAIL_PASSWORD`: Password of **App** that allowed to send email using you'r `EMAIL_HOST`.
- `EMAIL_PORT`: Just set it to default `587`.
- `EMAIL_USE_TLS`: For better security set it to `True`.
- `SEND_EMAIL`: Choose do you wan't to send email (`True`) or not (`False`).

**Redis variables:**

- `REDIS_HOST`: Means first part of redis address. For non production development set it to `"redis"`.
- `REDIS_PORT`: Default is `"6379"`, you can set it or another, it's up to you.
- `REDIS_DB`: Redis DB number. Set only allowed DB number. If DB number 1 is used, better to set it to 2, however setting it as DB 1 still allowed. Up to you. **DB number 0 is allowed**.

**Celery variables:**

- `CELERY_BROKER`: Celery message broker url. If you use Redis and deploy project locally use default: `"redis://redis:6379/0"`. Instead of 0 can be another DB number.
- `CELERY_RESULTS`: Celery results broker url. Same as `CELERY_BROKER` set default value if deploy locally: `"redis://redis:6379/0"`.

**Gunicorn variables:**
Note: Set it only if you actually use gunicorn. Currently gunicorn is hard to use on Windows or even unavailable. If you want to use gunicorn it should be linux or Docker container.

- `WEB_BING`: Binds server url. For local development set it to `"0.0.0.0:8000"`.
