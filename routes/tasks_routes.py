from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request, jsonify, Blueprint
from models.tasks_model import Task
from database import conn_cursor

conn, cursor = conn_cursor()
task_bp = Blueprint(
    "task",
    __name__,
    url_prefix="/api/tasks",
)


# create a task


@task_bp.route("/create", methods=["POST"])
@jwt_required()
def create(
    list_id=1,
):

    data = request.get_json()
    user_id_str = get_jwt_identity()

    title = data.get("title")
    if not title:
        return jsonify({"error": "Invalid title"}), 400

    description = data.get("description")
    if not description:
        return jsonify({"error": "Invalid description"}), 400

    end_date = data.get("end_date")
    if not end_date:
        return jsonify({"error": "Invalid end_date"}), 400

    priority_id = data.get("priority_id", '')
    status_id = data.get("status_id", '')

    register = Task(
        user_id=int(user_id_str),
        name=title,
        list_id=list_id,
        description=description,
        priority_id=priority_id,
        end_date=end_date,
        status_id=status_id,
    )
    if register.save_update(
        conn=conn,
        cursor=cursor,
    ):
        return jsonify({"success": "Task saved successfully"}), 201
    return jsonify({"error": "error saving task"}), 500
