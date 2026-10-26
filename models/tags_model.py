from datetime import datetime


class Tag:

    def __init__(
        self,
        user_id,
        name,
        tag_id=None,
        date_created=None,
        date_updated=None,
    ):
        self.user_id = user_id
        self.name = name
        self.tag_id = tag_id
        self.date_created = date_created
        self.date_updated = (
            date_updated if date_updated else datetime.now().strftime("%d/%m/%Y, %H:%M")
        )

    def save_update(self, conn, cursor):
        if not self.tag_id:
            try:
                cursor.execute(
                    "INSERT INTO tags (user_id,name,date_updated)VALUES(?,?,?)",
                    (
                        self.user_id,
                        self.name,
                        self.date_updated,
                    ),
                )
                conn.commit()
                self.tag_id = cursor.lastrowid
                return True

            except Exception as e:
                print(f"error saving tag")
                return False
        try:
            cursor.execute(
                "UPDATE tags SET name = ?, date_updated = ? WHERE id =?",
                (
                    self.name,
                    self.date_updated,
                    self.tag_id,
                ),
            )
            conn.commit()
            return True

        except Exception as e:
            print(f"error updating tag")
            return False

    # after saving if in case i need to return the tag

    def tag_dic(self):
        return {
            "tag_id": self.tag_id,
            "user_id": self.user_id,
            "name": self.name,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }

    @classmethod
    def find_tag(cls, cursor, tag_id):
        try:
            cursor.execute("SELECT * FROM tags WHERE id =?", (tag_id,))
            data = cursor.fetchone()
            if not data:
                return None
            (
                tag_id,
                user_id,
                name,
                date_created,
                date_updated,
            ) = data
            return cls(
                tag_id=tag_id,
                user_id=user_id,
                name=name,
                date_created=date_created,
                date_updated=date_updated,
            )
        except Exception as e:
            print(f"error fetching tag : { e }")
            return None
