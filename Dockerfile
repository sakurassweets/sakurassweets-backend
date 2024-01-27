#########################################################
###### Stage 1: Run linter and collect staticfiles ######
#########################################################
FROM python:3.12-alpine AS collectstatic

# Set work directory
WORKDIR /app

# Copy project
COPY core/ .

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Install linting tools
RUN pip install --upgrade pip
RUN pip install flake8

# Copy the project files from the collectstatic stage
COPY --from=collectstatic /app /app

# Lint the code
RUN flake8 --ignore=E501,F401 .

#########################################################
################ Stage 2: Runtime stage #################
#########################################################
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y ncat
RUN apt-get update -y \
    && apt-get install postgresql gcc python3-dev musl-dev -y

# Copy only requirements and install them
COPY core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files from the builder stage
COPY --from=builder /app /app

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1
