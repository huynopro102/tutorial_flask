FROM python:3.12.4-alpine
WORKDIR /app
COPY setup.txt ./
COPY src /app/