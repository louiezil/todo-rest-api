from flask import Blueprint, request, jsonify
from models.user_class import User
from database import conn_cursor
from werkzeug.security import generate_password_hash, check_password_hash
from utils.user_auth import check_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

conn, cursor = conn_cursor()
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth",
)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    error = None
    if request.method == "POST":
        data = request.get_json()
        name = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not name:
            error = "username is Empty..."
            return jsonify({"error": error})
        elif len(name) <= 3:
            error = "invalid username..."
            return jsonify({"error": error})

        if not email:
            error = "email is Empty..."
            return jsonify({"error": error})
        elif "@" not in email:
            error = "email must have an @ sign..."
            return jsonify({"error": error})
        elif len(email) <= 10:
            error = "invalid email address..."
            return jsonify({"error": error})

        if not password:
            error = "password is Empty..."
            return jsonify({"error": error})

        if not error:
            # check if user exists
            user_exists = check_user(cursor, name, email)
            if user_exists:
                error = "user Already Exist"
                return jsonify({"error": error})

            hashed_password = generate_password_hash(password)
            register = User(
                user_name=name,
                email=email,
                password=hashed_password,
            )
            if register.save_update_user(conn, cursor):
                return jsonify({"success": "User registered success"}), 201
            return jsonify({"error": "user registration failed..."}), 204


@auth_bp.route("/login", methods=["POST"])
def login():
    error = None
    # lets get the details
    if request.method == "POST":
        data = request.get_json()

        username = data.get("username")
        if not username or len(username) < 4:
            error = "Enter Valid username"
            return jsonify({"error": error})

        email = data.get("email")
        if not email or "@" not in email or len(email) < 10:
            error = "Enter Valid Email Address"
            return jsonify({"error": error})

        user_exist = check_user(
            cursor,
            username,
            email,
        )
        if user_exist:
            password = data.get("password")
            if not password or len(password) < 5:
                error = "Invalid Password input..."
                return jsonify({"error": error})

            db_password = user_exist[3]
            if check_password_hash(db_password, password):
                token = create_access_token(identity=str(user_exist[0]))
                return jsonify({"token": token}), 200
            error = "password Incorrect..."
            return jsonify({"error": error}), 204
        return (
            jsonify(
                {
                    "error": "user not found...",
                }
            ),
            204,
        )


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id_str = get_jwt_identity()
    print(user_id_str)

    user_id = int(user_id_str)

    user_found = User.find_user(cursor, user_id)
    if user_found:
        converted = user_found.convert()
        return jsonify(converted), 200
    return jsonify({"error": "user not found"}), 204
