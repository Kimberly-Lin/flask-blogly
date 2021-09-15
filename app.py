"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_users():
    """redirect to users page"""

    return redirect("/users")

@app.get("/users")
def load_user_list():
    """load user list page"""
    users=User.query.all()
    return render_template("user_list.html", users = users)


@app.get("/users/new")
def load_new_user_form():
    """load form to submit new user"""
    return render_template("create_user.html")

@app.post("/users/new")
def create_user_from_form():
    """process new user form and add new user in DB"""
    first_name = request.form("first_name")
    last_name = request.form("last_name")
    image_url = request.form("image_url")

    new_user = User(first_name,last_name,image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.get("/users/<int:user_id>")
def load_user_details_page(user_id):
    """load the user details for the selected user"""
    user = User.query.get(user_id)
    return render_template("user_detail.html", user=user)