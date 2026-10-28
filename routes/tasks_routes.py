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
    list_id=None,
):

    data = request.get_json()

    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)

    title = data.get("title")
    if not title:
        return jsonify({"error": "Invalid title"}), 400

    description = data.get("description", "")

    end_date = data.get("end_date", "")

    priority_id = data.get("priority_id", None)
    status_id = data.get("status_id", None)

    register = Task(
        user_id=user_id,
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
        return jsonify(register.convert_dic())
    return jsonify({"error": "error saving task"}), 500
