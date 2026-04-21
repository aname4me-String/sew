from __future__ import annotations

from flask import Flask

from controller import VerkehrController
from service import VerkehrService


def create_app() -> Flask:
    app = Flask(__name__)
    service = VerkehrService()
    controller = VerkehrController(service)
    app.register_blueprint(controller.blueprint)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
