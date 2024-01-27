
FROM python:3.12-alpine

# Set work directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y ncat
RUN apt-get update -y \
    && apt-get install postgresql gcc python3-dev musl-dev -y

# Copy only requirements and install them
COPY core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install linting tools
RUN pip install --upgrade pip
RUN pip install flake8

# Copy project
COPY core/ .

# Lint the code
RUN flake8 --ignore=E501,F401 .

# Run collectstatic
RUN python manage.py collectstatic --noinput

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1
