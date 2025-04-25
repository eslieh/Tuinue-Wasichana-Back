<<<<<<< HEAD

=======
from datetime import datetime
from .BaseModel import BaseModel
from sqlalchemy_serializer import SerializerMixin

class Donor(BaseModel):
    __tablename__ = "donors"

    serialize_rules = ('-donations.donor',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    is_anonymous = db.Column(db.Boolean, default=False)
    donation_frequency = db.Column(db.String(20), default='one-time')
    
    # Relationship with donations if needed
    donations = db.relationship('Donations', back_populates='donor')
>>>>>>> 7e73f8123acded6da5f43f186aec7af992fe2e99
