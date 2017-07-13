from __future__ import print_function

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col


# Some application and database setup. This should be taken care of
# elsewhere in an application and is not specific to the tables. See
# Flask-SQLAlchemy docs for more about what's going on for this first
# bit.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
# To suppress a warning. Not important.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# An example model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


# Create the database, and put some records in it.
db.create_all()

user1 = User('user1', 'test1@example.com')
user2 = User('user2', 'test2@example.com')

db.session.add(user1)
db.session.add(user2)
db.session.commit()


# Define a table, then pass in the database records
class UserTable(Table):
    username = Col('Username')
    email = Col('Email')

users = User.query.all()
print(UserTable(items=users).__html__())
