import os


class Config(object):
    APP_PORT = os.getenv("APP_PORT") or 3000
    APP_HOST = os.getenv("APP_HOST") or "0.0.0.0"
    KAFKA_URI = os.getenv("KAFKA_URI") or "localhost:9092"
    MONGO_URI = os.getenv("MONGO_URI") or "mongodb://admin:admin@localhost:27017"


class RunConfig(Config):
    DB_NAME = os.getenv("DB_NAME") or "teams"
    TOPIC = os.getenv("TOPIC") or "teams"


class TestConfig(Config):
    DB_NAME = "teams_test"
    TOPIC = "test_topic"


app_config = {
    "test": TestConfig,
    "run": RunConfig,
}
