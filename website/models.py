from . import db
from flask_login import UserMixin


# task schema
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(150))
    description = db.Column(db.String(500), nullable=True)
    #date_due = db.Column(db.Date(timezone-True), nullable=True )
    #completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# user schema
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    nickname = db.Column(db.String(150))
    tasks = db.relationship('Task')