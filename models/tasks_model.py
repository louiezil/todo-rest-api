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
        self.date_created = date_created
        self.date_updated = (
            date_updated if date_updated else datetime.now().strftime("%d/%m/%Y, %H:%M")
        )
        self.priority_name = priority_name if priority_name else ""
        self.status_name = status_name if status_name else ""

        "methods"

    def save_update(
        self,
        conn,
        cursor,
    ):
        if self.task_id:
            try:
                cursor.execute(
                    "UPDATE tasks SET user_id  = ? , name = ?, description = ? ,priority_id = ?, end_date = ? ,status_id = ?, date_updated = ? WHERE id = ?",
                    (
                        self.user_id,
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
            print(self.name,self.list_id,self.user_id,self.description,self.date_created,self.status_id)
            conn.commit()
            self.task_id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"error saving task:{e}")
            return False

    @classmethod
    def fetch_task_by_id(cls, cursor, task_id):
        try:
            cursor.execute("SELECT * FROM tasks WHERE id =?", (task_id,))
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
            return [
                {"id": tag[1], "tag": tag[0]} for tag in task_tags 
            ]
        except Exception as e:
            print(f"error fetching tags: {e}")
            return None
