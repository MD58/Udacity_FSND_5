# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import sys
import json
from flask import Flask, render_template, request, Response, flash, \
    redirect, jsonify, abort, url_for

from flask_moment import Moment
from auth import AuthError, requires_auth
from model import setup_db, Movie, Actor

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
setup_db(app)


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

#  Movies
#  ----------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the Casting Agency API!'})


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
def delete_movie(payload, id):
    movie = Movie.query.filter(Movie.id == id).first()

    if movie is None:
        abort(404)

    try:
        movie.delete()
    except Exception:
        movie.rollback()
        abort(500)
    finally:
        movie.close_session()

    return (jsonify({'success': True, 'delete': id}), 200)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):
    body = request.get_json()
    title = body.get('title')
    release_date = body.get('release_date')

    if title is None:
        abort(400)

    movie = Movie(title, release_date)

    try:
        movie.insert()
    except Exception:
        movie.rollback()
        abort(500)
    finally:
        movie.close_session()

    return (jsonify({'success': True, 'movie': movie.format()}), 200)


@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, id):
    movie = Movie.query.filter(Movie.id == id).first()

    if movie is None:
        abort(404)

    body = request.get_json()
    title = body.get('title')
    release_date = body.get('release_date')

    if title is None:
        abort(400)

    movie.title = title
    movie.release_date = release_date

    try:
        movie.update()
    except Exception:
        movie.rollback()
        abort(500)
    finally:
        movie.close_session()

    return (jsonify({'success': True, 'movie': movie.format()}), 200)


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
def delete_actor(payload, id):
    actor = Actor.query.filter(Actor.id == id).first()

    if actor is None:
        abort(404)

    try:
        actor.delete()
    except Exception:
        actor.rollback()
        abort(500)
    finally:
        actor.close_session()

    return (jsonify({'success': True, 'delete': id}), 200)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
    body = request.get_json()
    name = body.get('name')
    gender = body.get('gender')
    date_of_birth = body.get('date_of_birth')

    if name is None or gender is None or date_of_birth is None:
        abort(400)

    actor = Actor(name, gender, date_of_birth)

    try:
        actor.insert()
    except Exception:
        actor.rollback()
        abort(500)
    finally:
        actor.close_session()

    return (jsonify({'success': True, 'actor': actor.format()}), 200)


@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, id):
    actor = Actor.query.filter(Actor.id == id).first()

    if actor is None:
        abort(404)

    body = request.get_json()
    name = body.get('name')
    gender = body.get('gender')
    date_of_birth = body.get('date_of_birth')

    if name is None or gender is None or date_of_birth is None:
        abort(400)

    actor.title = name
    actor.gender = gender
    actor.date_of_birth = date_of_birth

    try:
        actor.update()
    except Exception:
        actor.rollback()
        abort(500)
    finally:
        actor.close_session()

    return (jsonify({'success': True, 'actor': actor.format()}), 200)

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
