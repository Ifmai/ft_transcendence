# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8003

WORKDIR /tournament-app

COPY . /tournament-app

# Install dependencies from requirements.txt
RUN apt-get update && apt-get install -y curl
RUN pip install --upgrade pip
RUN apt-get install -y --no-install-recommends postgresql-client
RUN pip install --no-cache-dir -r /tournament-app/requirements.txt
#RUN chmod +x /tools/microservice-run.sh

ENTRYPOINT [ "bash", "./tools/microservice-run.sh" ]
