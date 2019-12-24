from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask import jsonify
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def serialize(self, items):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'items': [i.serialize for i in items.filter_by(cat_id=self.id)]
        }


class Items(Base):
    __tablename__ = 'items'

    cat_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    cat = relationship(Categories)
    user = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'cat_id': self.cat_id,
            'description': self.description,
        }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
