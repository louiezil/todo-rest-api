from models.tags_model import Tag


def find_tags(cursor, user_id):
    try:
        cursor.execute("SELECT * FROM tags WHERE user_id = ?", (user_id,))
        tags = cursor.fetchall()
        if not tags:
            return None
        return [
            Tag(
                user_id=user_id,
                name=name,
                tag_id=tag_id,
                date_created=date_created,  #
                date_updated=date_updated,
            ).tag_dic()
            for (
                tag_id,
                user_id,
                name,
                date_created,
                date_updated,
            ) in tags
        ]
    except Exception as e:
        return []
