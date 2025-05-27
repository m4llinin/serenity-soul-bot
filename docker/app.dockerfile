FROM python:3.12

WORKDIR /app

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install ffmpeg

COPY ../ .

EXPOSE 8080