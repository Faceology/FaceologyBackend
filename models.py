from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from config import app, session

Base = declarative_base()

class Event(Base):
    __tablename__ = 'tb_event'
    event_id = Column('event_id', Integer, primary_key=True)
    name = Column('name', String(128))
    event_key = Column('event_key', String(128))

    def __init__(self, event_key):
        self.event_key = event_key

    def as_dict(self):
        return {
            'event_key' : self.event_key,
        }

class User(Base):
    __tablename__ = 'tb_user'
    user_id = Column('user_id', Integer, primary_key=True)
    name = Column('name', String(128))
    photo = Column('photo', String(255))

    def as_dict(self):
        return {
            'user_id' : self.user_id,
            'name' : self.name,
            'photo' : self.photo,
        }

class EmployerInfo(Base):
    __tablename__ = 'tb_employer_info'
    employer_info_id = Column('employer_info_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('tb_user.user_id'))
    event_id = Column('event_id', Integer, ForeignKey('tb_event.event_id'))

    def as_dict(self):
        return {
            'user_id' : self.user_id,
            'event_id' : self.event_id,
        }





