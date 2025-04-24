from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from models.BaseModel import BaseModel
from models.user import User  

class Charity(User):  
    __tablename__ = 'charities'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    organisation_name = Column(String(120), nullable=False)
    organisation_description = Column(Text, nullable=True)
    logo = Column(String(255), nullable=True)  
    approved = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    stories = relationship('Story', back_populates='charity')
    donations = relationship('Donation', back_populates='charity')
    inventories = relationship('Inventory', back_populates='charity')

    __mapper_args__ = {
        'polymorphic_identity': 'charity',
    }

    def __repr__(self):
        return f"<Charity {self.organisation_name}>"
