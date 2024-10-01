from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    photos = relationship("Photo", back_populates="owner")
    contest = relationship("Contest", back_populates="owner")

class Contest(Base):
    __tablename__ = "contests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="contest")
    photos = relationship("Photo", back_populates="contest")

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    photo = Column(String)
    name = Column(String)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    contest_id = Column(Integer, ForeignKey('contests.id'), nullable=True)
    owner = relationship("User", back_populates="photos")
    contest = relationship("Contest", back_populates="photos")
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)

