FROM python:3.9-slim-buster

RUN apt-get update; \
    /usr/local/bin/python -m pip install --upgrade pip; \
	rm -rf /var/lib/apt/lists/*

ENV PG_DATABASE=postgres\
    PG_USER=postgres\
    PG_PASSWORD=postgres

COPY . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python", "./pythweb.py" ]