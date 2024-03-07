import os


class Config(object):
    MONGO_URI = os.getenv('MONGO_URI') or 'mongodb://admin:admin@localhost:27017'
    DB_NAME = os.getenv('DB_NAME') or 'teams'
    APP_PORT = os.getenv('APP_PORT') or 3000
    APP_HOST = os.getenv('APP_HOST') or '0.0.0.0'


class RunConfig(Config):
    pass


class TestConfig(Config):
    MONGO_URI = 'Fake_Uri'


app_config = {
    'test': TestConfig,
    'run': RunConfig,
}
