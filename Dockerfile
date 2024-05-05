FROM python:3.11.9-alpine

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY src ./src
COPY app.py .
CMD [ "python3", "app.py"]

