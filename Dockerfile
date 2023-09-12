FROM python:3.9-slim-buster AS BUILD-STAGE

ENV HOME=/app/credit-api
WORKDIR $HOME

RUN useradd -m python

COPY requirements.txt $HOME/
COPY app $HOME/app
COPY run.py $HOME/

RUN pip3 install -r requirements.txt

RUN chown -R python:python $HOME

USER python

EXPOSE 5500

CMD ["gunicorn", "--bind", "0.0.0.0:5500", "--workers", "8", "app:create_app({\"dbname\": \"infnet\", \"user\": \"postgres\", \"password\": \"aquelasenha\", \"host\": \"192.168.1.107\", \"port\": \"5432\"})"]

