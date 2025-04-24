from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from .BaseModel import BaseModel

db = SQLAlchemy()

class Donations(BaseModel):
    __tablename__ = "donations"
    serialize_rules = ('-donor.donations', '-charity.donations')

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    is_recurring = db.Column(db.Boolean, default=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)

    # Relationships
    donor = db.relationship('Donor', back_populates='donations')
    charity = db.relationship('Charity', back_populates='donations')
