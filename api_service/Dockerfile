FROM python:3.11-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

RUN mkdir app
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install #--no-interaction

ADD . /app
