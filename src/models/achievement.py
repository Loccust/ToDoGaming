import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.db import db


class Achievement(db.Model):
  __tablename__ = "achievements"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  description = db.Column(db.String(200))
  user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)