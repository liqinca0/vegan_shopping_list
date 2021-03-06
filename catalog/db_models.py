#!/usr/bin/env python

import datetime
import re

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Db table for storing registered user information
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, index=True)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
        }


# Db table for storing categories
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, index=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

    @property
    def urlname(self):
        """For constructing url path segment, remove everything except
        alphanumeric characters from category name"""
        pattern = re.compile(r'[\W_]+')
        return pattern.sub('', self.name)


# Db table for storing category items
class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    title = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'created_date': self.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            'title': self.title,
            'description': self.description,
            'cat_id': self.cat_id
        }

    @property
    def urltitle(self):
        """For constructing url path segment, remove everything except
        alphanumeric characters from item title"""
        pattern = re.compile(r'[\W_]+')
        return pattern.sub('', self.title)


engine = create_engine('sqlite:///catalogWithOAuth.db')

Base.metadata.create_all(engine)
