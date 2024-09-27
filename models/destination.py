from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    trips = relationship('Trip', back_populates='destination')
