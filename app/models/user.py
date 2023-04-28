
from flask_login import UserMixin
from app import db

from . import Base

class User(Base, db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    picture = db.Column(db.String)
    login_first = db.Column(db.DateTime)
    login_latest = db.Column(db.DateTime)
