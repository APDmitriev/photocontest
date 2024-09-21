from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    photos = relationship("Photo", back_populates="owner")

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="photos")
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)