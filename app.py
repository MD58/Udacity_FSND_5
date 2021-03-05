# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import sys
import json
from flask import Flask, render_template, request, Response, flash, \
    redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, Column, String, Integer, create_engine, exc
from flask_migrate import Migrate
import datetime
from datetime import date
from flask_cors import CORS
from auth import AuthError, requires_auth

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Movie(db.Model):

    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = db.Column(db.DateTime(), nullable=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {'id': self.id, 'title': self.title,
                'release_date': self.release_date}


class Actor(db.Model):

    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    date_of_birth = db.Column(db.DateTime(), nullable=False)

    # For age: I'm adding date of birth,
    # and returning the calculated age in the format method.
    def __init__(self, name,
                 gender, date_of_birth):
        self.name = name
        self.gender = gender
        self.date_of_birth = date_of_birth

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
          (today.month, today.day) <
          (self.date_of_birth.month, self.date_of_birth.day)
          )

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.get_age()
        }


class MovieActor(db.Model):

    __tablename__ = 'MovieActor'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Actor.id'))


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

#  Movies
#  ----------------------------------------------------------------

@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.all()
    movie_short = [movie.format() for movie in movies]
    total_movies = len(movies)

    if total_movies == 0:
        abort(400)

    return jsonify({'success': True, 'movies': movie_short,
                   'total_movies': total_movies})


@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(id, payload):
    try:
        movie = Movie.query.filter(Movie.id == id).first()

        if movie is None:
            abort(404)

        movie.delete()

        return (jsonify({'success': True, 'delete': id}), 200)
    except:

        abort(500)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):
    try:
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is None:
            abort(400)

        movie = Movie(title, release_date)
        movie.insert()

        return (jsonify({'success': True, 'movie': movie.format()}),
                200)
    except:

        abort(500)


@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(id, payload):
    try:
        movie = Movie.query.filter(Movie.id == id).first()

        if movie is None:
            abort(404)

        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is None:
            abort(400)

        movie.title = title
        movie.release_date = release_date

        movie.update()

        return (jsonify({'success': True, 'movie': movie.format()}),
                200)
    except:

        abort(500)


#  Actors
#  ----------------------------------------------------------------

@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    actors = Actor.query.all()
    actor_short = [actor.format() for actor in actors]
    total_actors = len(actors)

    if total_actors == 0:
        abort(400)

    return jsonify({'success': True, 'actors': actor_short,
                   'total_actors': total_actors})


@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(id, payload):
    try:
        actor = Actor.query.filter(Actor.id == id).first()

        if actor is None:
            abort(404)

        actor.delete()

        return (jsonify({'success': True, 'delete': id}), 200)
    except:

        abort(500)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
    try:
        body = request.get_json()
        name = body.get('name', None)
        gender = body.get('gender', None)
        date_of_birth = body.get('date_of_birth', None)

        if name is None or gender is None or date_of_birth is None:
            abort(400)

        actor = Actor(name, gender, date_of_birth)
        actor.insert()

        return (jsonify({'success': True, 'actor': actor.format()}),
                200)
    except:

        abort(500)


@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(id, payload):
    try:
        actor = Actor.query.filter(Actor.id == id).first()

        if actor is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        gender = body.get('gender', None)
        date_of_birth = body.get('date_of_birth', None)

        if name is None or gender is None or date_of_birth is None:
            abort(400)

        actor.title = name
        actor.gender = gender
        actor.date_of_birth = date_of_birth

        actor.update()

        return (jsonify({'success': True, 'actor': actor.format()}),
                200)
    except:

        abort(500)

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:

if __name__ == '__main__':
    app.run()


# ----------------------------------------------------------------------------#
# Error Handlers.
# ----------------------------------------------------------------------------#

@app.errorhandler(400)
def bad_request(error):
    return (jsonify({'success': False, 'error': 400,
            'message': 'bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return (jsonify({'success': False, 'error': 404,
            'message': 'resource not found'}), 404)


@app.errorhandler(405)
def not_allowed(error):
    return (jsonify({'success': False, 'error': 405,
            'message': 'method not allowed'}), 405)


@app.errorhandler(422)
def unprocessable(error):
    return (jsonify({'success': False, 'error': 422,
            'message': 'unprocessable'}), 422)


@app.errorhandler(500)
def unprocessable(error):
    return (jsonify({'success': False, 'error': 500,
            'message': 'Internal Server Error'}), 500)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# ----------------------------------------------------------------------------#
# Application End.
# ----------------------------------------------------------------------------#
