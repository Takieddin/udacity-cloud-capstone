from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import ENUM
import json
import os

database_path = os.environ['DATABASE_URL']
#database_name = "capstone"
#database_path = "postgres://postgres:12345678@{}/{}".format(database_path, database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    actors = db.relationship('Actor',
                             secondary='assigning',
                             backref=db.backref('movies', lazy='dynamic'))

    def __init__(self, title, release_date, gender="male"):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}


class Actor(db.Model):
    __tablename__ = 'Actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    # gender = db.Column(db.String)
    gender = db.Column(
        db.Enum("female", "male", name="gender_enum", create_type=False))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}


assigning = db.Table('assigning',
                     db.Column('movie_id', db.Integer,
                               db.ForeignKey('Movie.id')),
                     db.Column('actor_id', db.Integer,
                               db.ForeignKey('Actor.id'))
                     )
