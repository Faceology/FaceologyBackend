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
            'eventId' : self.event_id,
            'eventKey' : self.event_key,
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
            'userId' : self.user_id,
            'name' : self.name,
            'photo' : self.photo,
        }

class EmployerInfo(Base):
    __tablename__ = 'tb_employer_info'
    employer_info_id = Column('employer_info_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('tb_user.user_id'))
    event_id = Column('event_id', Integer, ForeignKey('tb_event.event_id'))
    bio = Column('bio', String)
    headline = Column('headline', String)
    profile_link = Column('profile_link', String)
    email = Column('email', String)

    user_info = relationship('Entity')
    user_jobs = relationship('EmployerJob')

    def __init__(self, user_id, event_id, bio, headline, profile_link, email):
        self.user_id = user_id
        self.event_id = event_id
        self.bio = bio
        self.headline = headline
        self.profile_link = profile_link
        self.email = email

    def as_dict(self):
        return {
            'employerInfoId' : self.employer_info_id,
            'bio' : self.bio,
            'headline' : self.headline,
            'profileLink' : self.profile_link,
            'email' : self.email,
            'userInfo' : self.user_info.as_dict(),
            'userJobs' : map(lambda x: x.as_dict(), self.user_jobs)
        }

class EmployerJob(Base):
    __tablename__ = 'tb_employer_job'
    employer_job_id = Column('employer_job_id', Integer, primary_key=True)
    employer_info_id = Column('employer_info_id', Integer, ForeignKey('tb_employer_info.employer_info_id'))
    location = Column('location', String)
    title = Column('title', String)
    company_name = Column('company_name', String)
    date_start = Column('date_start', String)
    date_end = Column('date_end', String)
    is_current = Column('is_current', Boolean)

    def __init__(self, employer_info_id, location, title, company_name, date_start, date_end, is_current):
        self.employer_info_id = employer_info_id
        self.location = location
        self.title = title
        self.company_name = company_name
        self.date_start = date_start
        self.date_end = date_end
        self.is_current = is_current

    def as_dict(self):
        return {
            'location' : self.location,
            'title' : self.title,
            'companyName' : self.company_name,
            'dateStart' : self.date_start,
            'dateEnd' : self.date_end,
            'isCurrent' : self.is_current
        }




