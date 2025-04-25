from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .BaseModel import BaseModel

class Inventory(BaseModel):
    __tablename__ = 'inventories'

class Inventory(BaseModel, SerializerMixin):
    __tablename__ = 'inventories'
    
    serialize_rules = ('-charity.inventories',)
    
    id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)
    product = db.Column(db.String(100), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    beneficiary_name = db.Column(db.String(100), nullable=False)

    # Establishing the relationship with Charity
    charity = db.relationship("Charity", back_populates="inventories")
