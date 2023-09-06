FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5500", "--workers", "8", "app:create_app({\"dbname\": \"infnet\", \"user\": \"postgres\", \"password\": \"aquelasenha\", \"host\": \"192.168.1.107\", \"port\": \"5432\"})"]

EXPOSE 5500
