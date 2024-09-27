from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    itineraries = relationship('Itinerary', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'


class Itinerary(Base):
    __tablename__ = 'itineraries'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='itineraries')
    destinations = relationship('Destination', back_populates='itinerary')

    def __repr__(self):
        return f'<Itinerary {self.title}>'


class Destination(Base):
    __tablename__ = 'destinations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # Add extend_existing=True if 'destinations' table already exists
    __table_args__ = {'extend_existing': True}