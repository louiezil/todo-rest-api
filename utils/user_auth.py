def check_user(cursor, username, email) -> any | None:
    try:
        cursor.execute(
            "SELECT * FROM users WHERE user_name =? OR email = ? ",
            (
                username,
                email,
            ),
        )
        user = cursor.fetchone()
        if user:
            return user
        return None
    except Exception as e:
        print(f"error checking user :{e}")
        return None
