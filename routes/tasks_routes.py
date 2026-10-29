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


@task_bp.route("", methods=["POST"])
@jwt_required()
def create():

    data = request.get_json()

    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)

    title = data.get("title")
    if not title:
        return jsonify({"error": "Invalid title"}), 400

    list_id = data.get("list_id")
    description = data.get("description", "")
    end_date = data.get("end_date")
    priority_id = data.get("priority_id")
    status_id = data.get("status_id")

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
        return jsonify(register.convert_dic()), 201
    return jsonify({"error": "error saving task"}), 500


@task_bp.route("", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)
    user_tasks = []

    for each in Task.find_tasks_by_user(cursor, user_id):
        user_tasks.append(each.convert_dic())
    return jsonify(user_tasks), 200


@task_bp.route("<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):

    task = Task.fetch_task_by_id(cursor, task_id, user_id=int(get_jwt_identity()))
    if task:
        return jsonify(task.convert_dic()), 200
    return jsonify({"error": "task not found"}), 404


# 1. Get user_id from token
# 2. Find task (verify it belongs to user)
# 3. If not found → 404
# 4. Get JSON body (updated fields)
# 5. Update task
# 6. Return updated task


@task_bp.route("<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):

    user_id = int(get_jwt_identity())
    task = Task.fetch_task_by_id(cursor, task_id, user_id)
    if not task:
        return jsonify({"error": "task Not found"}), 404

    data = request.get_json()

    task.name = data["title"] if "title" in data else task.name
    task.description = (
        data["description"] if "description" in data else task.description
    )
    task.status_id = data["status_id"] if "status_id" in data else task.status_id
    task.priority_id = (
        data["priority_id"] if "priority_id" in data else task.priority_id
    )
    task.end_date = data["end_date"] if "end_date" in data else task.end_date

    if task.save_update(conn, cursor):
        return jsonify(task.convert_dic()), 200
    return jsonify({"error": "task update failed"}), 500


# 1. Get user_id from token
# 2. Find task (verify it belongs to user)
# 3. If not found → 404
# 4. Delete task
# 5. Return success message


@task_bp.route("<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete(task_id):
    user_id = int(get_jwt_identity())
    task = Task.fetch_task_by_id(cursor,task_id,user_id)
    if task:
        if task.find_and_del(conn, cursor):
            return jsonify({"success": "deletion success"}), 200
        return jsonify({"error": "error deleting task"}), 500
    return jsonify({"error": "task not found"}), 404
