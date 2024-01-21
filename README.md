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

- [Documentation](https://github.com/sakurassweets/sakurassweets-backend/docs)

### Installation

**Clone the repository:**

```bash
$ git clone https://github.com/sakurassweets/sakurassweets-backend
```

**Enter project folder:**

```bash
$ cd sakurassweets-backend
```

**Create virtual environment:**

```bash
$ python -m venv .venv
```

**Activate virtual environment:**

- For windows:

```bash
$ .venv\scripts\activate
```

- For linux:

```bash
$ source .venv\bin\activate
```

> you will see `(.venv)` before code line in terminal

**Enter core folder:**

```bash
$ cd core
```

**Install requirements:**

```bash
$ pip install -r requirements.txt
```

**[Create a PosgreSQL Database table](https://www.youtube.com/watch?v=oWsAYx2R9RI&ab_channel=Knowledge360) (This is optional, you can ignore it if you use sqlite3 DB)**

- **remember your _`username`_, _`password`_ and _`name`_ of db table you created**

**Setup the .env file (check next topic)**

**Provide migrations:**

```bash
$ python manage.py migrate
```

**Run redis server:**

For windows firstly you should install [WSL](https://learn.microsoft.com/ru-ru/windows/wsl/install).

Then using WSL/Linux terminal run:

```bash
$ redis-server
```

**Run celery worker:**

- For windows:

```bash
$ celery -A core worker -l info -P solo
```

- For linux:

```bash
$ celery -A core worker -l info
```

**Run project:**

```bash
$ python manage.py runserver
```

# The .env setup

Note: "0.0.0.0" as host means any IP used with provided port.

## DB setup (if using PosgreSQL):

- Find the `.env.example` file in project
- Rename it to `.env` and open
- Set _`DB_NAME`_, _`DB_USER`_, _`DB_PASS`_, to _`name`_, _`username`_ and _`password`_ that you've enetered on DB creation
- Set _`DB_HOST`_ to `localhost` if you deploy project locally
- Set _`DB_PORT`_ to `5432` (default for PostgreSQL)
- Set _`DB_ENGINE`_ to you'r backend for DB. Default is `"django.db.backends.postgresql"` for PostgreSQL.

## Other variables:

**Django variables:**

- `DJANGO_SECRET_KEY`: Randomly generated secret key, you can enter anything in there, but i recommend just generate it. Used in JWT generation.
- `DJANGO_ALLOWED_HOSTS`: Hosts that can actually host project. Just set it to: `localhost, 127.0.0.1, 0.0.0.0` for local deployment.
- `DEBUG`: Django debug mode. If something goes wrong django shows you debug message with problem. Set `1` to set it as `True`, and `0` for `False`
- `CSRF_TRUSTED`: Trusted origins for CSRF operations. For example sending some data through POST request from input form on website. Set it to: `http://localhost, http://127.0.0.1, http://0.0.0.0` for local deployment.
- `CORS_ORIGINS`: Origins that allowed to make requests through CORS validation. Set it to same as `CSRF_TRUSTED`.

**Email sending variables:**

Note: To use email sending read [this](), if you don't want to do this just set _`SEND_EMAIL`_ to `False`.

- `EMAIL_HOST`: In most cases the email from which emails will be sended to user.
- `EMAIL_PASSWORD`: Password of **App** that allowed to send email using you'r `EMAIL_HOST`.
- `EMAIL_PORT`: Just set it to default `587`.
- `EMAIL_USE_TLS`: For better security set it to `True`.
- `SEND_EMAIL`: Choose do you wan't to send email (`True`) or not (`False`).

**Redis variables:**

- `REDIS_HOST`: Means first part of redis address. For local development set it to `"127.0.0.1"`.
- `REDIS_PORT`: Default is `"6379"`, set it or another, it's up to you.
- `REDIS_DB`: Redis DB number. Set only allowed DB number. If DB number 1 is used, better to set it to 2, however setting it as DB 1 still allowed. Same, up to you. **DB number 0 is allowed**.

**Celery variables:**

- `CELERY_BROKER`: Celery message broker url. If you use Redis and deploy project locally use default: `"redis://127.0.0.1:6379/0"`. Instead of 0 can be another DB number.
- `CELERY_RESULTS`: Celery results broker url. Same as `CELERY_BROKER` set default value if deploy locally: `"redis://127.0.0.1:6379/0"`.

**Gunicorn variables:**
Note: Set it only if you actually use gunicorn. Currently gunicorn is hard to use on Windows or even unavailable. If you want to use gunicorn it should be linux or Docker container.

- `WEB_BING`: Binds server url. For local development set it to `"0.0.0.0:8000"`.
