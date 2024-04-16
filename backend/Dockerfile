# Base image
FROM python:3.12-slim

# Updates and setup
RUN apt-get -y update && apt-get -y upgrade
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p code
WORKDIR /code

# Development dependencies
RUN apt-get -y install netcat-openbsd

# Install application dependencies
COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Import app itself
COPY ./app app

# Start the app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]