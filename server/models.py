from sqlalchemy import Integer, String, Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    messages = relationship('Message', back_populates='sender')

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    sender_id = Column(Integer, ForeignKey('users.id'))

    sender = relationship('User', back_populates='messages')