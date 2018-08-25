from __future__ import print_function

from flask import Flask, url_for, request
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
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        return url_for('index', sort=col_key, direction='desc' if reverse else 'asc')


@app.route('/')
def index():
    sort_column = request.args.get('sort') or 'username'
    sort_reverse = request.args.get('direction') == 'desc'

    order_by = '{}{}'.format(sort_column, ' desc' if sort_reverse else '')

    users = User.query.order_by(order_by)
    table = UserTable(users, sort_by=sort_column, sort_reverse=sort_reverse)

    # You would usually want to pass this out to a template with
    # render_template.
    return table.__html__()

if __name__ == '__main__':
    app.run(debug=True)
