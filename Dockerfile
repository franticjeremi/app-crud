FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ARG APP_HOST=0.0.0.0
ARG APP_PORT=8000
CMD uvicorn main:app --host ${APP_HOST} --port ${APP_PORT}