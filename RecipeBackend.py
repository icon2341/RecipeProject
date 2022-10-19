"""
Flask Backend to the recipe project web interface
Author: Group 7 CSCI 320 01-02
"""
import SQLInterface
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

app = Flask(__name__)

app.config['SECRET_KEY'] = '3f07e17a6aca41b3409e6e84af01dfd62ec479a6df127cc58485de51e2488383'


# from flask import Flask, render_template
# from flask_restful import Api, Resource, reqparse
#
# app = Flask(__name__)
# api = Api(app)
#
#
# # temp function location
# def getUserSignUpForm():
#     print("LEMON")
#     return "<h1>DOGMA<h1>"
#
# @app.route('/')
# def tuna():
#     return render_template("SignUp.html", func= getUserSignUpForm)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign Up")


@app.route("/Login")
def Login():
    return render_template("Login.html")


@app.route("/SignUp", methods=["GET", 'POST'])
def SignUp():
    form = RegistrationForm()
    print("Test")
    # if form.validate_on_submit():
    if request.method == "POST":
        SQLInterface.create_user(form.username.data, form.email.data, form.password.data)

    return render_template("SignUp.html", form=form)


@app.route("/SignUp", methods=['POST'])
def signupuser():
    print(request.json)
    return "<div><hi/div>"


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
    return redirect("/Login", code=302)


app.run(host='0.0.0.0', port=80)
