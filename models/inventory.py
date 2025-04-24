from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

class Inventory(BaseModel):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.id'), nullable=False)
    product = db.Column(db.String(100), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    beneficiary_name = db.Column(db.String(100), nullable=False)

    # Establishing the relationship with Charity
    charity = db.relationship("Charity", back_populates="inventories")

    def __repr__(self):
        return f"<Inventory(id={self.id}, product={self.product}, quantity={self.product_quantity}, beneficiary={self.beneficiary_name})>"