FROM python:3.12

WORKDIR /app

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install ffmpeg sqlite3

RUN mkdir -p data && alembic upgrade head && /app/init_db.sh

COPY ../ .

EXPOSE 8080