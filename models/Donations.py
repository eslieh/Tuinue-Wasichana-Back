from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Donations(BaseModel):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Integer, nullable = False)
    is_recurring = db.Column(db.Boolean, default)