FROM python:3.11-slim

WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y pkg-config


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]