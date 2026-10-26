from datetime import datetime


class List:

    def __init__(
        self,
        user_id,
        description,
        date_created=None,
        date_updated=None,
        list_id=None,
    ):
        self.user_id = user_id
        self.description = description
        self.date_created = date_created
        self.date_updated = (
            date_updated
            if date_updated
            else datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        )
        self.list_id = list_id

    def save_update(self, conn, cursor):
        if self.list_id:
            try:
                cursor.execute(
                    "UPDATE lists SET description =?,date_updated =? WHERE id =?",
                    (
                        self.description,
                        self.date_updated,
                        self.list_id,
                    ),
                )
                conn.commit()
                return True

            except Exception as e:
                print(f"error with updating List : {e}")
                return False

        try:
            cursor.execute(
                " INSERT INTO lists (user_id , description , date_updated ) VALUES (? , ? , ?)",
                (
                    self.user_id,
                    self.description,
                    self.date_updated,
                ),
            )

            conn.commit()
            self.list_id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"error with updating List : {e}")
            return False

    # convert the object into dic

    def convert_dict(self):
        data = {
            "list_id": self.list_id,
            "user_id": self.user_id,
            "description": self.description,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }
        return data

    @classmethod
    def fetch_by_id(cls, cursor, list_id):
        try:
            cursor.execute("SELECT * FROM lists WHERE id =?", (list_id,))
            data = cursor.fetchone()
            if not data:
                return None
            (
                list_id,
                user_id,
                description,
                date_created,
                date_updated,
            ) = data
            return cls(
                list_id=list_id,
                user_id=user_id,
                description=description,
                date_created=date_created,
                date_updated=date_updated,
            )
        except Exception as e:
            print(f"fetching a list using @method failed :{e} ")
            return None
