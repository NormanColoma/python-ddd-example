FROM python:3.11.9-alpine AS base

WORKDIR /usr/src/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY app.py .

FROM base AS prod

RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-dev --no-interaction --no-ansi

CMD ["python3", "app.py"]

FROM base AS dev

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN poetry config virtualenvs.in-project true \
 && poetry install --no-root --no-interaction --no-ansi

ENTRYPOINT ["/entrypoint.sh"]
CMD ["poetry", "run", "python3", "app.py"]
