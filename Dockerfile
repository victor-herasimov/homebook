FROM python:3.12-slim

WORKDIR /usr/src/app

RUN mkdir media

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
