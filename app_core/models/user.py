from app_core.models import db
from app_core.models import BaseModel


class User(BaseModel):
    """Luu thong tin user"""
    __tablename__ = 'user'
    username = db.Column(db.String, primary_key=True, unique=True)
    email = db.Column(db.String, primary_key=True, unique=True)
    name = db.Column(db.String)
