from datetime import datetime


class User:

    def __init__(
        self,
        user_name,
        email,
        password,
        user_id=None,
        date_created=None,
        date_updated=None,
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.date_created = date_created
        self.date_updated = (
            date_updated
            if date_updated
            else datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        )

    def save_update_user(self, conn, cursor) -> bool:
        if self.user_id:
            try:
                cursor.execute(
                    "UPDATE users SET user_name = ?, email = ?,password = ? WHERE id =?",
                    (self.user_name, self.email, self.password, self.user_id),
                )
                conn.commit()
                return True

            except Exception as e:
                print(f"error updating user: {e}")
                return False

        try:

            cursor.execute(
                "INSERT INTO users(user_name,email,password,date_updated)VALUES(?,?,?,?)",
                (
                    self.user_name,
                    self.email,
                    self.password,
                    self.date_updated,
                ),
            )
            conn.commit()
            self.user_id = cursor.lastrowid
            return True

        except Exception as e:
            print(f"error saving user:{e}")
            return False

    @classmethod
    def find_user(cls, cursor, user_id):
        try:
            cursor.execute("SELECT * FROM users WHERE id =?", (user_id,))
            user = cursor.fetchone()
            if user:
                (
                    user_id,
                    user_name,
                    email,
                    password,
                    date_created,
                    date_updated,
                ) = user
                return cls(
                    user_id = user_id,
                    user_name=user_name,
                    email=email,
                    password = None,
                    date_created= date_created,
                    date_updated=date_updated,
                        )
            return None
        except Exception as e:
            print(f"error with fetch user:{e}")
            return None
        
        
        
    def convert(self):
        return {
            'user_id':self.user_id,
            'user_name':self.user_name,
            'email':self.email,
            'date_created':self.date_created,
            'date_updated':self.date_updated,
        }