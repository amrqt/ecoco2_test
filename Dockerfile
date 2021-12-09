FROM python:3.9


RUN mkdir /code
WORKDIR /code

ENV PATH "${PATH}:/code/.local/bin"

RUN groupadd co2 \
    && useradd -r -g co2 -s /sbin/nologin -d /code co2

COPY requirements.txt manage.py .env ./
ADD ./ecotest ./ecotest
RUN chown -R co2:co2 .

RUN pip install -U pip

USER co2

RUN pip install -r requirements.txt --user