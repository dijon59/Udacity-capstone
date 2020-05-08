from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

# from sqlalchemy.orm import relationship
import os

# database_name = 'capstone_db'
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://localhost:5432/capstone_db')

db = SQLAlchemy()


# print(DATABASE_URI)
def setup_db(app, path_db=DATABASE_URL):
    # app.config.from_object('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = path_db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# def db_drop_and_create_all():
# db.drop_all()

# db_drop_and_create_all()

# relation table
helper_table = db.Table(
    'helper_table',
    sa.Column(
        'actor_id',
        sa.Integer,
        sa.ForeignKey('actor.id'),
        primary_key=True
    ),
    sa.Column(
        'movie_id',
        sa.Integer,
        sa.ForeignKey('movie.id'),
        primary_key=True
    )
)


# Movie

class Movie(db.Model):
    __tablename__ = 'movie'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String())
    release_date = sa.Column(sa.DateTime())
    actors = db.relationship(
        'Actor',
        secondary=helper_table,
        backref=db.backref('movies', lazy='dynamic')
    )

    def movie_information_format(self):
        actor_ids = [artists_ids[0] for artists_ids in
                     db.session.query(helper_table).filter(helper_table.c.movie_id == self.id).all()]
        if actor_ids:
            casts = [Actor.query.get(i).name for i in actor_ids]
        else:
            casts = []

        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'cast': casts
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


# Actor

class Actor(db.Model):
    __tablename__ = 'actor'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(), nullable=False)
    age = sa.Column(sa.Integer)
    gender = sa.Column(sa.String(10))

    def actor_information_format(self):
        movie_ids = [movie_ids[1] for movie_ids in
                     db.session.query(helper_table).filter(helper_table.c.actor_id == self.id).all()]
        if movie_ids:
            in_movies = [Movie.query.get(i).title for i in movie_ids]
        else:
            in_movies = []

        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'played_in_movies': in_movies
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
