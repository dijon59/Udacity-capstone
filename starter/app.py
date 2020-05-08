from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db, setup_db, Actor, Movie


def create_app(test_config=None):
    # configure app
    # os.environ("SQLALCHEMY_DATABASE_URI") = "postgresql://postgres:puru2000@localhost/casting_agency"
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    Migrate(app, db)

    @app.route('/')
    def index():
        return "API tests for Casting Agency project"

    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response

    @app.route('/actors', methods=['GET'])
    @requires_auth(permission='get:actors')
    def actors():
        """
            Returns a list of actors
        """
        try:
            actors_list = [actor.actor_information_format() for actor in Actor.query.order_by(Actor.id).all()]

            return jsonify({
                'success': True,
                'actors': actors_list
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors():
        """
        Posts actors and movie played by the actors
        """
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']
        played_in_movies = request.get_json()['movies']

        actor = Actor(name=name, age=age, gender=gender)

        for movie in played_in_movies:
            actor.movies.append(Movie.query.get(movie))

        actor.insert()

        return jsonify({
            "success": True,
            "status_code": 200,
            "actor": actor.actor_information_format()
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(actor_id):
        """
        Updates actors data
        """
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']
        played_in_movies = request.get_json()['movies']
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        if played_in_movies:
            actor.movies = []
            actor.update()

            for movie in played_in_movies:
                actor.movies.append(Movie.query.get(movie))

        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender
        actor.update()

        return jsonify({
            "success": True,
            "status_code": 200,
            "actor": actor.actor_information_format()
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actors(actor_id):
        """
        deletes actors data
        """
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        actor.delete()

        return jsonify({"success": True,
                        "status_code": 200,
                        "status_message": 'OK',
                        "id_deleted": actor_id})

    # Movie Routes

    @app.route('/movies', methods=["GET"])
    @requires_auth('get:movies')
    def movies():
        """
        Returns a list of movies
        """
        try:
            movies_list = [movie.movie_information_format()
                           for movie in Movie.query.order_by(Movie.id).all()]
            return jsonify({
                "success": True,
                "status_code": 200,
                "status_message": 'OK',
                "movies": movies_list
            })
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movies():
        """
        Posts movies and actors that play in the movies
        """
        title = request.get_json()['title']
        release_date = request.get_json()['release_date']
        actors = request.get_json()['actors']

        if title is None:
            abort(422)

        movie = Movie(title=title, release_date=release_date)

        for i in actors:
            movie.actors.append(Actor.query.get(i))

        movie.insert()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movie": movie.movie_information_format()
        })

    @app.route('/movies/<int:movie_id>', methods=['GET', 'PATCH'])
    @requires_auth(permission='patch:movies')
    def update_movies(movie_id):
        """
        Updates movies data
        """
        title = request.get_json()['title']
        release_date = request.get_json()['release_date']
        cast = request.get_json()['cast']
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        if cast:
            movie.actors = []
            movie.update()
            for person in cast:
                movie.actors.append(Actor.query.get(person))

        if title:
            movie.title = title
        if release_date:
            movie.release_date = release_date
        movie.update()

        return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "movie": movie.movie_information_format()
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movies(movie_id):
        """
        deletes movies data
        """
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)
        movie.delete()

        return jsonify({"success": True,
                        "status_code": 200,
                        "status_message": 'OK',
                        "id_deleted": movie_id})

    # Error Handeling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "status_message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "status_message": "resource Not found"
        }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(error.error), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
