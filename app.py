import logging
from flask import Flask

from src.infraestructure.config.config import Config
from src.infraestructure.rest.error_handler import handle_exception
from src.infraestructure.rest.team_controller import team_controller
from src.container import Container

logging.basicConfig(level=logging.INFO, format='{"dateTime": "%(asctime)s", "level": "info", "message": "%(message)s"}',
                    datefmt='%Y-%m-%d %H:%M:%S')


def create_app():
    flask_app = Flask(__name__)
    flask_app.register_blueprint(team_controller, url_prefix='/teams')
    flask_app.register_error_handler(Exception, handle_exception)
    container = Container()
    flask_app.container = container
    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.APP_HOST, port=Config.APP_PORT)
