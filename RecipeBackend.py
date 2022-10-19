"""
Flask Backend to the recipe project web interface
Author: Group 7 CSCI 320 01-02

RUNNING INSTRUCTIONS:

if in pycharm
you can do "cntl + shift + f10" and it will attempt to run this file and create a run config, that will run the flask server
note you will need to run

COPY PASTE THIS INTO YOUR TERMINAL (ALT-F12):

pip install flask-wtf flask wtforms flask_sqlalchemy SQLAlchemy

"""

import SQLInterface
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from Forms import *

app = Flask(__name__)

# this is a config file, need this for some security crap, not relevant I think, but makes it run happy
app.config['SECRET_KEY'] = '3f07e17a6aca41b3409e6e84af01dfd62ec479a6df127cc58485de51e2488383'

# Demonstration of how to connect to the postgres server
# Todo make this work
username = "group7"
password = "password"
db_name = "db_name"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/{db_name}"

db = SQLAlchemy(app)

#
"""
Example code, this is a Table (can be called anything). This is not the same as the postgresql table in our remote server
this essentially is a client-side representation of what the server looks like for querying purposes. For each new table
in SQL, you will have have one of these to define it. Feel free to change it up.
"""


# class Table(db.model):

# table is named users
#    __tablename__ = "users"
# the "id" (should be called username ig) attribute is added (a column)
#    id = db.Column(db.Integer, primary_key=True)
# Each route designates how to get to each page from
# the site
@app.route("/wonk", methods=["GET"])  # This is a demo of how a get request from a table might work
def wonk():
    pass
    # posts = Table.query.all
    # return render_template("Home.html", posts=posts)


"""
login route for when user attempts to log in button
"""


@app.route("/Login", methods=["GET", 'POST'])  # GET method is for going to the page, POST is for getting data
# from the user
def Login():
    form = LoginForm()
    # if button is pressed, post is sent, this listens and its all gooooooood manananna
    if request.method == "POST":
        if form.validate_on_submit():
            print(f"Welcome back: {form.username.data}, your password is {form.password.data}")
            # login_user(user)
        return redirect('/Home')
    return render_template("Login.html", form=form)


@app.route("/SignUp", methods=["GET", "POST"])
def SignUp():
    # the object we created above
    form = RegistrationForm()
    if request.method == "POST":  # We would like to use this but it might not work so oh well
        if form.validate_on_submit():
            SQLInterface.create_user(form.username.data, form.email.data, form.password.data)  # Example of how you
        # guys might wanna call a function with the database to create a user

    return render_template("SignUp.html", form=form)


# TODO BELOW IS NOT DONE
@app.route("/Pantry")
def Pantry():
    return render_template("Pantry.html")


@app.route("/Recipes")
def Recipes():
    return render_template("Recipes.html")


@app.route("/Home")
def Home():
    return render_template("Home.html")


@app.route("/Settings")
def Settings():
    return render_template("Settings.html")


@app.route("/")
def FrontPage():
    return redirect("/Login", code=302)  # Redirects the user from one site to another


# This command actually runs the server on port 80
app.run(host='0.0.0.0', port=80)
