"""
Flask Backend to the recipe project web interface
Author: Group 7 CSCI 320 01-02
"""
import datetime
import uuid

from flask import render_template, request, redirect
from flask_login import login_user, login_required, logout_user, current_user

from RecipeProject import app, bcrypt
from RecipeProject.DatabaseEntities import get_user_by_username
from RecipeProject.Forms import *


# Login Route
@app.route("/Login", methods=["GET", 'POST'])  # GET method is for going to the page, POST is for getting data
# from the user
def Login():
    form = LoginForm()
    # if button is pressed, post is sent, this listens and its all gooooooood manananna
    if request.method == "POST":
        if form.validate_on_submit():
            print(form.username.data, form.password.data)
            user = get_user_by_username(form.username.data)
            if user.valid():
                print(form.password.data, user['password'])
                if bcrypt.check_password_hash(user['password'], form.password.data):
                    print(f"Welcome back: {form.username.data}, your password is {form.password.data}")
                    login_user(user)
                    return redirect('/Home')
    return render_template("Login.html", form=form)


@app.route("/SignUp", methods=["GET", "POST"])
def SignUp():
    # the object we created above
    form = RegistrationForm()
    if request.method == "POST":  # We would like to use this but it might not work so oh well
        if form.validate_on_submit():
            # Hashing the password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            # Creating the user object
            user = User(
                uuid=str(uuid.uuid4()),
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                create_datetime=str(datetime.datetime.now()),
                last_access=str(datetime.datetime.now())
            )
            user.create_user()
            # flash(f"Welcome to Ryan Gosling {form.username.data}", "success")

            return redirect("/Login")

    return render_template("SignUp.html", form=form)


# TODO Implement stuff below
@app.route("/Pantry")
@login_required
def Pantry():
    return render_template("Pantry.html")


@app.route("/Recipes")
@login_required
def Recipes():
    return render_template("Recipes.html")


@app.route("/Home")
@login_required
def Home():
    print(current_user.data["username"])
    return render_template("Home.html", user=current_user.data["username"])


@app.route("/Settings")
@login_required
def Settings():
    return render_template("Settings.html", user=current_user.data["username"])


@app.route("/")
def FrontPage():
    return redirect("/Login", code=302)  # Redirects the user from one site to another


@app.route("/Logout")
@login_required
def Logout():
    logout_user()
    return redirect("/Login")


# This command actually runs the server on port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
