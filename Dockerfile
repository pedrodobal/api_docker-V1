FROM python:3.9-slim-buster

ENV HOME=/app/credit-api

WORKDIR $HOME

RUN useradd -m python

COPY requirements.txt $HOME/
COPY app $HOME/app
COPY run.py $HOME/
COPY db-init-scripts $HOME/db-init-scripts

RUN pip3 install -r requirements.txt

RUN chown -R python:python $HOME

USER python

EXPOSE 5500

CMD ["gunicorn", "--bind", "0.0.0.0:5500", "--workers", "8", "run:create_application()"]


