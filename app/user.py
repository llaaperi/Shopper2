from flask_login import UserMixin

from app.db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, picture):
        self.id = id_
        self.name = name
        self.email = email
        self.picture = picture

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], picture=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.execute(
            "INSERT INTO users (id, name, email, picture) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()
