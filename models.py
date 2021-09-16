from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.sql.schema import ForeignKey

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User (db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                    nullable=False)
    last_name = db.Column(db.String(50),
                    nullable=False)
    img = db.Column(db.Text, default="https://i.stack.imgur.com/l60Hf.png")

    


class Post (db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(150),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.DateTime,
                    nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    user = db.relationship('User',
                            backref='posts')