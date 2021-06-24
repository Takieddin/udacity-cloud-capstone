import os
import math
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, assigning, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    ITEMS_PER_PAGE = 100

    def paging(data, page):
        start = ITEMS_PER_PAGE*(page-1)
        end = (start + ITEMS_PER_PAGE)
        d = data[start:end]
        return d

    @app.route('/actors')
    @requires_auth(permission='get:actors_and_movies')
    def get_actors(p):
        page = request.args.get('page', 1, type=int)
        actors_data = Actor.query.order_by(Actor.id).all()
        if page > (len(actors_data)//ITEMS_PER_PAGE):
            page = (len(actors_data)//ITEMS_PER_PAGE)
            if (len(actors_data) % ITEMS_PER_PAGE) != 0:
                page += 1
        actors = [q.format() for q in actors_data]
        ap = paging(actors, page)
        return jsonify({
            'success': True,
            'actors': ap,
            'totalActors': len(actors)
        }), 200

    @app.route('/movies')
    @requires_auth(permission='get:actors_and_movies')
    def get_movies(p):
        page = request.args.get('page', 1, type=int)
        movies_data = Movie.query.order_by(Movie.id).all()
        if page > (len(movies_data)//ITEMS_PER_PAGE):
            page = (len(movies_data)//ITEMS_PER_PAGE)
            if (len(movies_data) % ITEMS_PER_PAGE) != 0:
                page += 1
        movies = [q.format() for q in movies_data]
        mp = paging(movies, page)
        return jsonify({
            'success': True,
            'movies': mp,
            'totalMovies': len(movies)
        }), 200

    

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='add:actor')
    def add_actor(p):

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if gender not in ['male', 'female'] or int(age) < 0:
            abort(400)
        actor = Actor(name, age, gender)
        actor.insert()
        return jsonify({
            'success': True,
            'totalActors': len(Actor.query.all())
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='add:movie')
    def add_movie(p):

        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        if title is None:
            abort(400)
        movie = Movie(title, release_date)
        movie.insert()
        return jsonify({
            'success': True,
            'totalMovies': len(Movie.query.all())

        }), 200

    @app.route('/movies/<int:movie_id>/edit', methods=['PATCH'])
    @requires_auth(permission='modify:movie')
    def update_movie(p, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        # for k in body.keys():
        #    movie[k]=body[k]
        if 'title' in body.keys():
            movie.title = body['title']
        if 'release_date' in body.keys():
            movie.release_date = body['release_date']
        movie.update()
        m = []
        m.append(movie.format())
        return jsonify({
            'success': True,
            "movie": m
        }), 200

    @app.route('/actors/<int:actor_id>/edit', methods=['PATCH'])
    @requires_auth(permission='modify:actor')
    def update_actor(p, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()
        # for k in body.keys():
        #    movie[k]=body[k]
        if 'name' in body.keys():
            actor.name = body['name']
        if 'age' in body.keys():
            actor.age = body['age']
        if 'gender' in body.keys():
            actor.gender = body['gender']
        actor.update()
        a = []
        a.append(actor.format())
        return jsonify({
            'success': True,
            'actor': a
        }), 200

    @app.route('/actors/<int:actor_id>/movies')
    @requires_auth(permission='get:actors_and_movies')
    def get_actor_movies(p, actor_id):
        page = request.args.get('page', 1, type=int)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        am = [m.format() for m in actor.movies]
        return jsonify({
            'success': True,
            'movies': paging(am, page)
        }), 200

    @app.route('/movies/<int:movie_id>/actors')
    @requires_auth(permission='get:actors_and_movies')
    def get_movie_actors(p, movie_id):
        page = request.args.get('page', 1, type=int)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        ma = [a.format() for a in movie.actors]
        return jsonify({
            'success': True,
            'actors': paging(ma, page)
        }), 200

    @app.route('/assigning', methods=['POST'])
    @requires_auth(permission='add:actor')
    def assign_actor_to_movie(p):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == body['actor_id']).one_or_none()
        movie = Movie.query.filter(Movie.id == body['movie_id']).one_or_none()
        if movie is None or actor is None:
            abort(422)
        if body["method"] == "assign":
            actor.movies.append(movie)
        elif body["method"] == "unassign":
            actor.movies.remove(movie)
        db.session.commit()
        return jsonify({
            'success': True,
            'actor': body['actor_id'],
            'movie': body['movie_id']
        }), 200
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actor')
    def delete_actor(p, actor_id):
        q = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if q is None:
            abort(404)
        q.delete()
        return jsonify({

            'success': True,
            'deleted': actor_id,
            'totalActors': len(Actor.query.all())
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movie')
    def delete_movie(p, movie_id):
        q = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if q is None:
            abort(404)
        q.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id,
            'totalMovies': len(Movie.query.all())
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def AuthError_invalid(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
