from flask import Blueprint, jsonify

users_blueprint = Blueprint("users", __name__, url_prefix="/users")


@users_blueprint.get("")
def list_users():
    return jsonify(
        {
            "users": [
                {
                    "id": 1,
                    "name": "Starter User",
                    "email": "starter@example.com",
                }
            ]
        }
    ), 200
