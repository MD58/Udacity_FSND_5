import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from datetime import date

db = SQLAlchemy()


def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


class BaseClass(db.Model):

    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def close_session(self):
        db.session.close()


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Movie(BaseClass):

    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = db.Column(db.DateTime(), nullable=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {'id': self.id, 'title': self.title,
                'release_date': self.release_date}


class Actor(BaseClass):

    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    date_of_birth = db.Column(db.DateTime(), nullable=False)

    # For age: I'm adding date of birth,
    # and returning the calculated age in the format method.

    def __init__(
        self,
        name,
        gender,
        date_of_birth
    ):

        self.name = name
        self.gender = gender
        self.date_of_birth = date_of_birth

    def get_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (
                self.date_of_birth.month, self.date_of_birth.day))

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.get_age(),
            }


class MovieActor(BaseClass):

    __tablename__ = 'MovieActor'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Actor.id'))
