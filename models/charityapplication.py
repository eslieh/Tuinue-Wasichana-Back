from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

class CharityApplication(BaseModel):
    __tablename__ = "charityapplications"

    id = db.Column(db.Integer, primary_key = True)
    organistaion_name = db.Column(db.String, nullable = False)
    organistaion_description = db.Column(db.String, nullable = False)
    status = db.Column(db.String, default = "pending")
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Organisation name : {self.organistaion_name} || Description {self.organistaion_description}"