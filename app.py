"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)


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
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    if (not first_name or not last_name):
        flash("Please enter a first and last name")
        return redirect("/users/new")

    new_user = User(first_name = first_name, last_name = last_name, img= image_url)
    #TODO: DEFAULT IMAGE NOT WORKING
    
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def load_user_details_page(user_id):
    """load the user details for the selected user"""
    user = User.query.get(user_id)
    return render_template("user_detail.html", user=user)

@app.get("/users/<int:user_id>/edit")
def load_user_edit_info_page(user_id):
    """load the edit user form for the selected user"""
    user = User.query.get(user_id)
    return render_template("edit_user.html", user=user)

@app.post("/users/<int:user_id>/edit")
def submit_edit_form(user_id):
    """process the edit form and return user to /users page"""
    user= User.query.get(user_id)
    breakpoint()

    if (request.form["first_name"]):
        user.first_name = request.form["first_name"]

    if (request.form["last_name"]):
        user.last_name = request.form["last_name"]
        
    if (request.form["image_url"]):
        user.img = request.form["image_url"]

    db.session.commit()

    return redirect("/users")

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete user from database, rediret back to users page"""

    user=User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
