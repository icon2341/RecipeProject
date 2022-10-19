"""
Flask Backend to the recipe project web interface
Author: Group 7 CSCI 320 01-02
"""

import SQLInterface
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
#from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '3f07e17a6aca41b3409e6e84af01dfd62ec479a6df127cc58485de51e2488383'


# Demonstration of how to connect to the postgres server
# Todo make this work
username = "group7"
password = "password"
db_name = "db_name"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/{db_name}"

db = SQLAlchemy(app)

class Table(db.model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

# Login form
# Each form shows how the form on the webpage will be set up, and what constraints to put on them
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) # validators tell you
    # what must happen Ex: Datarequired means you need that bit filled out, length means it must be a certain length
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In") # Submit button

# Registration Form
# same thing as above, but more in depth because the actual registration form, has more steps
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")


# Each route designates how to get to each page from
# the site
@app.route("/wonk", methods=["GET"]) # This is a demo of how a get request from a table might work
def wonk():
    posts = Table.query.all
    return render_template("Home.html", posts=posts)

"""
login route for when user attempts to log in button
"""
@app.route("/Login", methods=["GET", 'POST']) # GET method is for going to the page, POST is for getting data
# from the user
def Login():
    form = LoginForm()
    if request.method == "POST":

       # login_user(user)
        return redirect('/Home')
    return render_template("Login.html")


@app.route("/SignUp", methods=["GET", 'POST'])
def SignUp():
    form = RegistrationForm()
    # if form.validate_on_submit(): # We would like to use this but it might not work so oh well
    if request.method == "POST":
        SQLInterface.create_user(form.username.data, form.email.data, form.password.data) # Example of how you
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
    return redirect("/Login", code=302) # Redirects the user from one site to another

# This command actually runs the server on port 80
app.run(host='0.0.0.0', port=80)
