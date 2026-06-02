from flask import Flask

from app.controllers.users_controller import users_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(users_blueprint)

    @app.get("/health")
    def health_check() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    return app
