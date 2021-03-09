import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from setup.database import Database
from routing import RouteHandler
from src.lib.api.flask_error import BadRequest


def initialize_app():

    flask_app = Flask(__name__)
    flask_app.config.from_pyfile('./config/default.py')
    flask_app.config["PROPAGATE_EXCEPTIONS"] = True
    flask_app.config['JWT_SECRET_KEY'] = 'HEYEGE733GGDGEHJ3HH'

    route = RouteHandler(flask_app)
    route.setup()

    jwt = JWTManager(app=flask_app)

    return flask_app


app = initialize_app()
db = Database()


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    print(error)
    """Catch BadRequest exception globally, serialize into JSON, and respond with 400."""
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400


if __name__ == "__main__":
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)