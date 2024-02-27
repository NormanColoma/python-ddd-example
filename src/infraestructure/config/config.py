import os


class Config(object):
    MONGO_URI = os.getenv('MONGO_URI') or 'mongodb://admin:admin@localhost:27017'
    DB_NAME = os.getenv('DB_NAME') or 'teams'


class RunConfig(Config):
    pass


class TestConfig(Config):
    MONGO_URI = 'Fake_Uri'


app_config = {
    'test': TestConfig,
    'run': RunConfig,
}
