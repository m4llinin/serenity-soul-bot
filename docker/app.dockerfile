FROM python:3.12

WORKDIR /app

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install ffmpeg sqlite3

COPY ../ .

ENV DB_PATH="data/database.db"
RUN mkdir -p /app/data && chmod 777 /app/data

RUN alembic upgrade head

RUN chmod +x init_db.sh && ./init_db.sh

EXPOSE 8080