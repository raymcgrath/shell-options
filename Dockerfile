# Image from dockerhub
FROM python:3.11.8-slim 

ENV PYTHONUNBUFFERED 1
# Expose the port 8000 in which our application runs
EXPOSE 8000 
# Make /app as a working directory in the container
WORKDIR /app 

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
# Copy requirements from host, to docker container in /app 
COPY ./requirements.txt .

#Copy the supervisord configuration file
COPY supervisord.conf .

# Copy everything from ./src directory to /app in the container
COPY ./src . 
# Install the dependencies
RUN pip install -r requirements.txt 

CMD ["supervisord", "-c", "supervisord.conf"]