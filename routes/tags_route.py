from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.tags_model import Tag
from database import conn_cursor
from utils.tags_utils import find_tags

conn, cursor = conn_cursor()
tags_bp = Blueprint("tags", __name__, url_prefix="/api/tags")


@tags_bp.route("", methods=["POST"])
@jwt_required()
def create_tag():
    data = request.get_json()
    user_id = int(get_jwt_identity())

    Tag_name = data.get("name")
    if not Tag_name:
        return jsonify({"error": "Invalid Input"}), 400
    tag_found = Tag.find_by_userid_name(
        cursor,
        name=Tag_name,
        user_id=user_id,
    )
    if tag_found:
        print(tag_found.tag_dic())
        return jsonify({"error": "tag Already Exists.."}), 409
    Tag(
        user_id=user_id,
        name=Tag_name,
    ).save_update(
        conn,
        cursor,
    )
    return jsonify({"success": f"Tag Name:{Tag_name}, saved Successfully..."}), 201


@tags_bp.route("/<int:tag_id>", methods=["GET"])
@jwt_required()
def get_tag(tag_id):
    user_id = int(get_jwt_identity())

    tag = Tag.find_tag(cursor, tag_id)
    if tag and tag.user_id == user_id:
        return jsonify(tag.tag_dic())
    elif not tag:
        return jsonify({"error": "tag Not Found..."}), 404
    else:
        return jsonify({"error": "Unauthorized Access to Tag.."}), 403


@tags_bp.route("/<int:tag_id>", methods=["PUT"])
@jwt_required()
def update_tag(tag_id):

    user_id = int(get_jwt_identity())
    tag = Tag.find_tag(
        cursor,
        tag_id,
    )
    if tag and tag.user_id == user_id:
        data = request.get_json()
        tag_name = data["name"]
        if not tag_name:
            return jsonify({"error": "Invalid Input..."}), 400
        tag.name = tag_name
        if tag.save_update(
            conn,
            cursor,
        ):
            return jsonify(tag.tag_dic()), 200
        else:
            return jsonify({"error": "error with server"}), 500
    elif not tag:
        return jsonify({"error": "tag Not Found..."}), 404
    else:
        return jsonify({"error": "Unauthorized Tag Access..."}), 403


@tags_bp.route("<int:tag_id>", methods=["DELETE"])
@jwt_required()
def delete_tag(tag_id):
    user_id = int(get_jwt_identity())
    tag = Tag.find_tag(
        cursor,
        tag_id,
    )
    if tag and tag.user_id == user_id:
        tag.find_delete(
            conn,
            cursor,
            tag_id,
        )
        return (
            jsonify({"success": f" tag Name: {tag.name} , deleted successfully..."}),
            200,
        )
    elif not tag:
        return jsonify({"error": "Tag Not Found..."}), 404
    else:
        return jsonify({"error": "Unauthorized Tag Access..."}), 403


@tags_bp.route("", methods=["GET"])
@jwt_required()
def get_tags():
    user_id = int(get_jwt_identity())
    user_tags = find_tags(cursor, user_id)
    if user_tags:
        return jsonify(user_tags), 200
    return jsonify({"error": "tags Not Found..."}), 404
