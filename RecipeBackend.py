"""
Flask Backend to the recipe project web interface
Author: Group 7 CSCI 320 01-02
"""
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/Login")
def Login():
    return render_template("Login.html")

@app.route("/SignUp")
def SignUp():
    return render_template("SignUp.html")

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


app.run(port=80)
