import logging
import threading

from flask import Flask

from src.container import Container
from src.infraestructure.config.config import Config
from src.infraestructure.rest.error_handler import handle_exception

logging.basicConfig(
    level=logging.INFO,
    format='{"dateTime": "%(asctime)s", "level": "info", "message": "%(message)s"}',
    datefmt="%Y-%m-%d %H:%M:%S",
)


def create_app():
    flask_app = Flask(__name__)
    flask_app.register_blueprint(Container.team_controller().routes(), url_prefix="/teams")
    flask_app.register_error_handler(Exception, handle_exception)
    return flask_app


def start_consumers():
    bus = Container.event_bus()
    bus.listen()


if __name__ == "__main__":
    t1 = threading.Thread(target=start_consumers)
    t1.daemon = True
    t1.start()

    app = create_app()
    app.run(host=Config.APP_HOST, port=Config.APP_PORT)
