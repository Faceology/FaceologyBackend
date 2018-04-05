from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from config import app, session
from matching import find_best_match

Base = declarative_base()

class Event(Base):
    __tablename__ = 'tb_event'
    event_id = Column('event_id', Integer, primary_key=True)
    name = Column('name', String(128))
    event_key = Column('event_key', String(128))

    def __init__(self, event_key, name):
        self.event_key = event_key
        self.name = name

    def as_dict(self):
        return {
            'event_id' : self.event_id,
            'event_key' : self.event_key,
            'name' : self.name
        }

class Entity(Base):
    __tablename__ = 'tb_user'
    user_id = Column('user_id', Integer, primary_key=True)
    name = Column('name', String(128))
    photo = Column('photo', String(255))

    def __init__(self, name, photo):
        self.name = name
        self.photo = photo

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
    bio = Column('bio', String)

    user_info = relationship('Entity')

    # update when we have more info to add
    def __init__(self, user_id, event_id, bio):
        self.user_id = user_id
        self.event_id = event_id
        self.bio = bio

    def as_dict(self):
        return {
            'user_id' : self.user_id,
            'event_id' : self.event_id,
            'bio' : self.bio,
            'user_info' : self.user_info.as_dict()
        }





