from datetime import datetime


class Task:

    def __init__(
        self,
        user_id,
        name,
        list_id,
        task_id=None,
        description=None,
        priority_id=None,
        end_date=None,
        status_id=None,
        date_created=None,
        date_updated=None,
        list_name=None,
        priority_name=None,
        status_name=None,
    ):
        self.user_id = user_id
        self.name = name
        self.list_id = list_id
        self.task_id = task_id
        self.description = description if description else None
        self.priority_id = priority_id if priority_id else None
        self.end_date = end_date if end_date else None
        self.status_id = status_id if status_id else None
        self.date_created = (
            datetime.now().strftime("%d/%m/%Y, %H:%M") if not task_id else date_created
        )
        self.date_updated = (
            date_updated if date_updated else datetime.now().strftime("%d/%m/%Y, %H:%M")
        )
        self.priority_name = priority_name if priority_name else ""
        self.status_name = status_name if status_name else ""
        self.list_name = list_name
        "methods"

    def save_update(
        self,
        conn,
        cursor,
    ):
        if self.task_id:
            try:
                cursor.execute(
                    "UPDATE tasks SET name = ?, description = ? ,priority_id = ?, end_date = ? ,status_id = ?, date_updated = ? WHERE id = ?",
                    (
                        self.name,
                        self.description,
                        self.priority_id,
                        self.end_date,
                        self.status_id,
                        self.date_updated,
                        self.task_id,
                    ),
                )
                conn.commit()
                return True
            except Exception as e:
                print(f"error updating task:{e}")
                return False
        try:
            cursor.execute(
                "INSERT INTO tasks (list_id,user_id,name,description,priority_id,end_date,status_id,date_updated)VALUES(?,?,?,?,?,?,?,?)",
                (
                    self.list_id,
                    self.user_id,
                    self.name,
                    self.description,
                    self.priority_id,
                    self.end_date,
                    self.status_id,
                    self.date_updated,
                ),
            )
            conn.commit()
            self.task_id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"error saving task:{e}")
            return False

    @classmethod
    def fetch_task_by_id(cls, cursor, task_id, user_id):
        try:
            cursor.execute(
                "SELECT * FROM tasks WHERE id =? AND user_id =? ",
                (
                    task_id,
                    user_id,
                ),
            )
            data = cursor.fetchone()
            if data:
                (
                    task_id,
                    list_id,
                    user_id,
                    name,
                    description,
                    priority_id,
                    end_date,
                    status_id,
                    date_created,
                    date_updated,
                ) = data
                return cls(
                    task_id=task_id,
                    list_id=list_id,
                    user_id=user_id,
                    name=name,
                    description=description,
                    priority_id=priority_id,
                    end_date=end_date,
                    status_id=status_id,
                    date_created=date_created,
                    date_updated=date_updated,
                )
            return None
        except Exception as e:
            print(f"error fetching task:{ e }")
            return None

    def convert_dic(self):
        return {
            "task_id": self.task_id,
            "list_id": self.list_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "priority_id": self.priority_id,
            "end_date": self.end_date,
            "status_id": self.status_id,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "list_name": self.list_name,
            "priority_name": self.priority_name,
            "status_name": self.status_name,
        }

    def find_task_tags(self, cursor):
        try:
            cursor.execute(
                """
        SELECT tags.name,
                        tags.id
                        
        FROM tags
        LEFT JOIN task_tags ON task_tags.tag_id = tags.id
        WHERE task_tags.task_id =?
        """,
                (self.task_id,),
            )
            task_tags = cursor.fetchall()
            return [{"id": tag[1], "tag": tag[0]} for tag in task_tags]
        except Exception as e:
            print(f"error fetching tags: {e}")
            return None

    @classmethod
    def find_tasks_by_user(cls, cursor, user_id):
        try:
            cursor.execute(
                """
        SELECT tasks.*,
                    lists.description AS list_description,
                    statuses.name AS status_name,
                    priorities.name AS priority_name
        FROM tasks
        LEFT JOIN lists ON lists.id = tasks.list_id
        LEFT JOIN statuses ON  statuses.id  = tasks.status_id
        LEFT JOIN priorities ON priorities.id = priority_id
        WHERE tasks.user_id =?
        ORDER BY tasks.date_created DESC
        
        """,
                (user_id,),
            )
            user_tasks = cursor.fetchall()
            return [
                cls(
                    task_id=task_id,
                    list_id=list_id,
                    user_id=user_id,
                    name=name,
                    description=description,
                    priority_id=priority_id,
                    end_date=end_date,
                    status_id=status_id,
                    date_created=date_created,
                    date_updated=date_updated,
                    list_name=list_description,
                    priority_name=priority_name,
                    status_name=status_name,
                )
                for (
                    task_id,
                    list_id,
                    user_id,
                    name,
                    description,
                    priority_id,
                    end_date,
                    status_id,
                    date_created,
                    date_updated,
                    list_description,
                    status_name,
                    priority_name,
                ) in user_tasks
            ]

        except Exception as e:
            print(f"error with fetching tasks by user: {e}")
            return []

    # @classmethod
    def find_and_del(self, conn, cursor):
        if self.fetch_task_by_id(cursor,self.task_id,self.user_id):
            try:
                    cursor.execute("DELETE from tasks WHERE id =?", (self.task_id,))
                    conn.commit()
                    return True

            except Exception as e:
                print(f"error with deletion:{e}")
                return False
        return False
