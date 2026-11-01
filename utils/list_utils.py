from models.lists_class import List


def find_user_lists(cursor, user_id):
    try:
        cursor.execute("SELECT * FROM lists WHERE lists.user_id = ?", (user_id,))
        lists = cursor.fetchall()
        if lists:
            return [
                List(
                    list_id=list_id,
                    user_id=user_id,
                    description=description,
                    date_created=date_created,
                    date_updated=date_updated,
                ).convert_dict()
                for (
                    list_id,
                    user_id,
                    description,
                    date_created,
                    date_updated,
                ) in lists
            ]
        return []

    except Exception as e:
        print(f"error fetching user lists:{e}")
        return []
