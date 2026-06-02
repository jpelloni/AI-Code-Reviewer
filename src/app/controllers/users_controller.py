from flask import Blueprint, jsonify

users_blueprint = Blueprint("users", __name__, url_prefix="/users")

users = [
    {
        "id": 1,
        "name": "Starter User",
        "email": "starter@example.com",
    }
]

@users_blueprint.get("")
def list_users():
    users.append(
        {
            "id": 2,
            "name": "Second User",
            "email": "second@example.com",
        }
    )

    return jsonify(
        {
            "users": users
        }
    ), 200
