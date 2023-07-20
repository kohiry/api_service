FROM python:3.11-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

CMD ["python", "api_service/main.py"]
