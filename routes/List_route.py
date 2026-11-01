from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.lists_class import List
from database import conn_cursor
from utils.list_utils import find_user_lists

conn, cursor = conn_cursor()
list_bp = Blueprint(
    "list",
    __name__,
    url_prefix="/api/lists",
)


@list_bp.route("", methods=["POST"])
@jwt_required()
def create_list():
    user_id = int(get_jwt_identity())

    data = request.get_json()

    description = data.get("description")
    if List.fetch_by_userid_description(
        cursor,
        user_id,
        description,
    ):
        return jsonify({"error": "list Already exist"}), 409
    List(
        user_id,
        description,
    ).save_update(
        conn,
        cursor,
    )
    return jsonify({"success": "list saved successfully..."}), 201


@list_bp.route("<int:list_id>", methods=["PUT"])
@jwt_required()
def update(list_id):
    user_id = int(get_jwt_identity())
    data = List.fetch_by_id(cursor, list_id)
    if data and data.user_id == user_id:
        json_data = request.get_json()

        updated_description = json_data["description"]
        if not updated_description:
            return jsonify({"error": "Invalid Description"}), 400

        data.description = updated_description
        data.save_update(conn, cursor)
        return jsonify(data.convert_dict()), 200
    elif not data:
        return jsonify({"error": "No data Found"}), 404
    else:
        return jsonify({"error": "user doesn't Own List..."}), 403


@list_bp.route("<int:list_id>", methods=["GET"])
@jwt_required()
def get_list(list_id):
    user_id = int(get_jwt_identity())

    list_exist = List.fetch_by_id(
        cursor,
        list_id,
    )
    if not list_exist:
        return jsonify({"error": "List not Found..."}), 404

    if list_exist and list_exist.user_id == user_id:
        return jsonify(list_exist.convert_dict())
    return jsonify({"error": "user doesn't Own List"}), 403


@list_bp.route("/<int:list_id>", methods=["DELETE"])
@jwt_required()
def delete_list(list_id):
    user_id = int(get_jwt_identity())

    list_exist = List.fetch_by_id(cursor, list_id)

    if list_exist and list_exist.user_id == user_id:
        list_exist.find_delete(
            conn,
            cursor,
            list_id,
        )
        return (
            jsonify(
                {"success": f"list Name:{list_exist.description}, deleted success"}
            ),
            200,
        )
    elif not list_exist:
        return jsonify({"error": "List Not found..."}), 404
    else:
        return jsonify({"error": "Unauthorized deletion.."}), 403


@list_bp.route("", methods=["GET"])
@jwt_required()
def get_lists():
    user_id = int(get_jwt_identity())
    user_lists = find_user_lists(cursor, user_id)
    if not user_lists:
        return jsonify({"error": "No data Found"}), 404
    return jsonify(user_lists)
