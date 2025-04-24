from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()

class Inventory(Base, SerializerMixin):
    __tablename__ = 'inventories'

    # Specify which relationships to serialize
    serialize_rules = ('-charity.inventories',)

    id = Column(Integer, primary_key=True)
    charity_id = Column(Integer, ForeignKey('charities.id'), nullable=False)
    product = Column(String(100), nullable=False)
    product_quantity = Column(Integer, nullable=False)
    beneficiary_name = Column(String(100), nullable=False)

    # Establishing the relationship with Charity
    charity = relationship("Charity", back_populates="inventories")

    def __repr__(self):
        return f"<Inventory(id={self.id}, product={self.product}, quantity={self.product_quantity}, beneficiary={self.beneficiary_name})>"