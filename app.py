import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # @app.route('/')
    # def getInfo():
    #     return jsonify({"message": "This is the Casting Agency Project By Farah"})

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()

        if actors is None:
            abort(400)

        formatted_actors = [actor.format()
                            for actor in actors]

        return jsonify({
            'success': True,
            'actors': formatted_actors
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()

        if movies is None:
            abort(400)
        formatted_movies = [movie.format()
                            for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatted_movies
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if name == '' or age == '' or gender == '':
            abort(422)

        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title == '' or release_date == '':
            abort(422)

        movie = Movie(
            title=title,
            release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        body = request.get_json()
        new_age = body.get('age', None)

        actor = Actor.query.filter_by(
            id=actor_id).one_or_none()

        if actor is None:
            abort(404)

        actor.age = new_age
        actor.update()

        return jsonify({
            'success': True,
            'id': actor.id,
            'age': actor.age
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        body = request.get_json()

        new_title = body.get('title', None)

        movie = Movie.query.filter_by(
            id=movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.title = new_title
        movie.update()

        return jsonify({
            'success': True,
            'id': movie.id,
            'title': movie.title
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):

        actor = Actor.query.get(actor_id)

        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'actor_id': actor_id
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'movie_id': movie_id
        })

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(err):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['code']
        }), 403

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=8080, debug=True)
