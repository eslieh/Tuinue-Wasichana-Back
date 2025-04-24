from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from BaseModel import Base  



class Charity(User):  
    __tablename__ = "charities"
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)  
    organisation_name = Column(String(120), nullable=False)
    organisation_description = Column(Text, nullable=True)
    logo = Column(String(255), nullable=True)  # path or URL
    approved = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stories = relationship('Story', back_populates='charity')  
    donations = relationship('Donation', back_populates='charity')  
    inventories = relationship('Inventory', back_populates='charity')  

    __mapper_args__ = {
        'polymorphic_identity': 'charity',
    }

    def __repr__(self):
        return f"<Charity {self.organisation_name}>"
