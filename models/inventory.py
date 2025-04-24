from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

<<<<<<< HEAD
class Inventory(BaseModel, SerializerMixin):
    __tablename__ = 'inventories'

    # Specify which relationships to serialize
    serialize_rules = ('-charity.inventories',)

    id = db.Column(Integer, primary_key=True)
    charity_id = db.Column(Integer, db.ForeignKey('charities.id'), nullable=False)
    product = db.Column(String(100), nullable=False)
    product_quantity = db.Column(Integer, nullable=False)
    beneficiary_name = db.Column(String(100), nullable=False)
=======
class Inventory(BaseModel):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)
    product = db.Column(db.String(100), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    beneficiary_name = db.Column(db.String(100), nullable=False)
>>>>>>> development

    # Establishing the relationship with Charity
    charity = db.relationship("Charity", back_populates="inventories")

    def __repr__(self):
        return f"<Charity {self.organisation_name}>"
