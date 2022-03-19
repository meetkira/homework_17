# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from models import Movie, Director, Genre
from schema import MovieShema, DirectorShema, GenreShema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

movie_schema = MovieShema()
movies_schema = MovieShema(many=True)

director_schema = DirectorShema()
directors_schema = DirectorShema(many=True)

genre_schema = GenreShema()
genres_schema = GenreShema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if genre_id and director_id:
            movies = db.session.query(Movie).filter(Movie.director_id == director_id, Movie.genre_id == genre_id).all()
        elif director_id:
            movies = db.session.query(Movie).filter(Movie.director_id == director_id).all()
        elif genre_id:
            movies = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()
        else:
            movies = Movie.query.all()

        return movies_schema.dump(movies), 200

    def post(self):
        try:
            movie_data = request.json
            movie = Movie(**movie_data)
            with db.session.begin():
                db.session.add(movie)
            return "", 201
        except Exception:
            return "", 400


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == mid).one()
            return movie_schema.dump(movie), 200
        except Exception:
            return "", 404

    def put(self, mid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == mid).one()
        except Exception:
            return "", 404

        try:
            movie_data = request.json
            movie.title = movie_data.get("title")
            movie.description = movie_data.get("description")
            movie.trailer = movie_data.get("trailer")
            movie.year = movie_data.get("year")
            movie.rating = movie_data.get("rating")
            movie.genre_id = movie_data.get("genre_id")
            movie.director_id = movie_data.get("director_id")

            db.session.add(movie)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 400

    def delete(self, mid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == mid).one()
            db.session.delete(movie)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 404


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    def post(self):
        try:
            director_data = request.json
            director = Director(**director_data)
            with db.session.begin():
                db.session.add(director)
            return "", 201
        except Exception:
            return "", 400


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            director = db.session.query(Director).filter(Director.id == did).one()
            return director_schema.dump(director), 200
        except Exception:
            return "", 404

    def put(self, did: int):
        try:
            director = db.session.query(Director).filter(Director.id == did).one()
        except Exception:
            return "", 404

        try:
            director_data = request.json
            director.name = director_data.get("name")

            db.session.add(director)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 400

    def delete(self, did: int):
        try:
            director = db.session.query(Director).filter(Director.id == did).one()
            db.session.delete(director)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 404


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200

    def post(self):
        try:
            genre_data = request.json
            genre = Genre(**genre_data)
            with db.session.begin():
                db.session.add(genre)
            return "", 201
        except Exception:
            return "", 400


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == gid).one()
            return genre_schema.dump(genre), 200
        except Exception:
            return "", 404

    def put(self, gid: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == gid).one()
        except Exception:
            return "", 404

        try:
            director_data = request.json
            genre.name = director_data.get("name")

            db.session.add(genre)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 400

    def delete(self, gid: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == gid).one()
            db.session.delete(genre)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 404


if __name__ == '__main__':
    app.run(debug=True)
