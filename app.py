import logging
from flask import Flask
from infraestructure.rest.error_handler import handle_exception
from infraestructure.rest.team_controller import team_controller

app = Flask(__name__)
app.register_blueprint(team_controller)
app.register_error_handler(Exception, handle_exception)

logging.basicConfig(level=logging.INFO, format='{"dateTime": "%(asctime)s", "level": "info", "message": "%(message)s"}',
                    datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    app.run()
