import uuid

from werkzeug.security import check_password_hash, generate_password_hash

from src.models.db import db


class User(db.Model):
    id = db.Column(db.String(36),
                   primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    xp = db.Column(db.Integer, default=0)

    tasks = db.relationship("Task", backref="user", lazy=True)
    achievements = db.relationship("Achievement", backref="user", lazy=True)

    def __init__(self, username):
        self.username = username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)