from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

class Admin (User):
    __tablename__ "admin"

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __repr__(self):
        return f"Admin : {self.id}"
