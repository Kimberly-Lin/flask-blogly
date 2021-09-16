"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension
import datetime


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
    user = User.query.get(user_id)
    user_posts = user.posts
    
    for post in user_posts:
        db.session.delete(post)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>/posts/new")
def load_post_form(user_id):
    """Direct user to add post form"""
    user=User.query.get(user_id)
    return render_template("post_form.html", user = user)

@app.post("/users/<int:user_id>/posts/new")
def add_post(user_id):
    """Add post to database"""
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title = title, content = content, 
                    created_at = datetime.datetime.now(), 
                    user_id = user_id)
    
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def show_post(post_id):
    """Show post details"""
    post = Post.query.get(post_id)
  
    return render_template("post_detail.html", post=post)
    
@app.get("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """Show edit post form"""
    post = Post.query.get(post_id)
    return render_template("edit_post.html", post=post)

@app.post("/posts/<int:post_id>/edit")
def submit_edit_post(post_id):
    """process the edit form and return user to /users page"""
    post = Post.query.get(post_id)
    
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete post from database, redirect back to posts page"""
    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")