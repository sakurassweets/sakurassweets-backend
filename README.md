# Sakuras Sweets

Welcome to the Sakuras Sweets! Below are instructions on setting up and running the project API locally

## Technology stack used
### Build with:
<img src="https://img.shields.io/badge/Django-0c4b33?logo=django&logoColor=white&style=ShieldStyle" /> <img src="https://img.shields.io/badge/Django%20Rest%20Framework-a30000?logo=django&logoColor=white&style=ShieldStyle" /> <img src="https://img.shields.io/badge/SwaggerUI-85ea2d?logo=swagger&logoColor=black&style=ShieldStyle" /> <img src="https://img.shields.io/badge/Docker-ffffff?logo=docker&logoColor=White&style=ShieldStyle" />
### Version Control and Development Tools used:
<img src="https://img.shields.io/badge/Git-DC4936?logo=git&logoColor=white&style=ShieldStyle" /> <img src="https://img.shields.io/badge/GitHub-1A1C1E?logo=github&logoColor=white&style=ShieldStyle" /> <img src="https://img.shields.io/badge/Visual Studio Code-0C72C5?logo=visual studio code&logoColor=white&style=ShieldStyle" />

## Getting Started

### Prerequisites
- [Python](https://www.python.org/) (v3.12.0 or later)
- [PostgreSQL](https://www.postgresql.org/) (v16 or later)

### Installation
- Clone the repository:
```bash
$ git clone https://github.com/sakurassweets/sakurassweets-backend
```

- Enter project folder:
```bash
$ cd sakurassweets-backend
```

- Create virtual environment:
```bash
$ python -m venv .venv
```

- Activate virtual environment:
```bash
$ .venv\scripts\activate
```
  you will see `(.venv)` before code line in terminal

- Enter core folder:
```bash
$ cd core
```

- Install requirements:
```bash
$ pip install -r core/requirements.txt
```

- [Create a PosgreSQL Database table](https://www.youtube.com/watch?v=oWsAYx2R9RI&ab_channel=Knowledge360) (This is optional, you can ignore it to use sqlite3 DB)

  **remember your _`username`_, _`password`_ and _`name`_ of db table you created**
- Setup the .env file (check next topic)

- Provide migrations:
```bash
$ python manage.py migrate
```

- Run project:
```bash
$ python manage.py runserver
```

# The .env setup
## DB setup (if using PosgreSQL):
- Find the `.env.example` file in project
- Rename it to `.env` and open
- Set _`DB_NAME`_, _`DB_USER`_, _`DB_PASS`_, to _`name`_, _`username`_ and _`password`_ that you've enetered on DB creation
- Set _`DB_HOST`_ to `localhost` if you deploy project locally
- Set _`DB_PORT`_ to `5432` (default for PostgreSQL)
## Other variables
- `DJANGO_SECRET_KEY`: Randomly generated secret key, you can enter anything in there, but i recommend just generate it. Used in JWT generation
- `DJANGO_ALLOWED_HOSTS`: Hosts that can actually host project. Just set it to: `localhost,127.0.0.1` for local deployment (don`t type any whitespaces)
- `DEBUG`: Django debug mode. If something goes wrong django shows you debug message with problem. Set `1` to set it as `True`, and `0` for `False`
- `CSRF_TRUSTED`: Trusted origins for CSRF operations. For example sending some data through POST request from input form on website. Set it to: `http://localhost,http://127.0.0.1` for local deployment
- `CORS_ORIGINS`: Origins that allowed to make requests through CORS validation. Set it to same as `CSRF_TRUSTED`
