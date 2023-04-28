from app import db

class Base(object):
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    deleted = db.Column(db.DateTime)

from .user import User
