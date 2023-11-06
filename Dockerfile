# pull official base image
FROM python:3.12

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get install -y ncat
RUN apt-get update -y \
    && apt-get install postgresql gcc python3-dev musl-dev -y

# lint
RUN pip install --upgrade pip
RUN pip install flake8

# install dependencies
COPY core/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY core/ .

RUN flake8 --ignore=E501,F401 .

COPY ./nginx.conf /etc/nginx/conf.d/

EXPOSE 80

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:80"]