from __future__ import annotations

from flask import Flask

from controller import Controller
from service import Service


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(Controller(Service()).blueprint)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
