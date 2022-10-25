"""
Flask Backend to the recipe project web interface
Author: Group 7 CSCI 320 01-02
"""
import datetime

from flask import render_template, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from RecipeProject import sql
from RecipeProject import app, bcrypt, login_manager
from RecipeProject.DatabaseEntities import get_user_by_username, User, get_recipe_by_id, Recipe, get_recipe_if_owned
from RecipeProject.Forms import *

# Redirects logged out users to front page
login_manager.login_view = "Login"


# Login Route
@app.route("/Login", methods=["GET", 'POST'])  # GET method is for going to the page, POST is for getting data
# from the user
def Login():
    form = LoginForm()
    # if button is pressed, post is sent, this listens and its all gooooooood manananna
    if request.method == "POST":
        if form.validate_on_submit():
            user = get_user_by_username(form.username.data)
            if user.valid():
                if bcrypt.check_password_hash(user['password'], form.password.data):
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
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                create_datetime=str(datetime.datetime.now()),
                last_access=str(datetime.datetime.now())
            )
            user.create_user()
            # flash(f"Welcome to Ryan Gosling {form.username.data}", "success")

            return redirect("/Home")

    return render_template("SignUp.html", form=form)


@app.route("/Pantry")
@login_required
def Pantry():
    form = IngredientSearch()
    # Todo implement functions for the search system
    pantry = [{"item_name": "Yo mama",
               "quantity_bought": 1,
               "current_quantity": 1,
               "purchase_date": "rn",
               "expiration_date": "never",
               "unit_of_measure": "tons"},
              {"item_name": "Yo mama",
               "quantity_bought": 1,
               "current_quantity": 1,
               "purchase_date": "rn",
               "expiration_date": "never",
               "unit_of_measure": "tons"}
              ]
    return render_template("Pantry.html", user=current_user, pantry=pantry, form=form)


@app.route("/MyRecipes")
@login_required
def myRecipes():
    limit = 10  # Limit of the number of recipes returned
    recipes = [Recipe(sql_data=data) for data in
               sql.get_all_query(f"SELECT * FROM recipe WHERE uid={current_user['uuid']} LIMIT {limit}")]

    return render_template("MyRecipes.html", user=current_user, recipes=recipes)


@app.route("/Home")
@login_required
def Home():
    return render_template("Home.html", user=current_user)


@app.route("/NewIngredient")
@login_required
def NewIngredient():
    return render_template("NewIngredient.html", user=current_user)


@app.route("/Settings", methods=["GET", "POST"])
@login_required
def Settings():
    form = ResetPassword()
    if request.method == "POST":
        if form.validate_on_submit():
            sql.query("UPDATE \"User\" SET password=%s WHERE uid=%s;",
                      (bcrypt.generate_password_hash(form.new_password.data).decode('utf-8'), current_user['uuid']))
    return render_template("Settings.html", user=current_user, form=form)


@app.route("/")
def FrontPage():
    return redirect("/Login", code=302)  # Redirects the user from one site to another


@app.route("/Logout")
@login_required
def Logout():
    logout_user()
    return redirect("/Login")

@app.route("/newRecipe", methods=["GET", "POST"])
@login_required
def NewRecipe():

    #TODO need to add form piping for new recipe
    # Query constructor

    return render_template("NewRecipe.html", user=current_user)

@app.route("/editRecipe", methods=["GET", "POST"])
@login_required
def EditRecipe():
    form = RecipeEditing()
    recipe_id = request.args.get("rId")
    if request.method == "GET":
        recipe = get_recipe_if_owned(recipe_id, current_user["uuid"])
        if recipe is not None:

            form.servings.data = float(recipe["servings"])
            form.title.data = recipe["recipe_name"]
            form.difficulty.data = float(recipe["difficulty"])
            form.prep_time.data = recipe["cook_time"]
            form.category.data = recipe['category']
            form.steps.data = recipe['steps']
            form.description.data = recipe['description']

            return render_template("EditRecipe.html", user=current_user, form=form)
        # Non valid recipe id
        else:
            return redirect("/MyRecipes")
    elif request.method == "POST":
        # TODO update database with form values
        sql_query = "UPDATE recipe SET "
        sql.query()
        return render_template("EditRecipe.html", user=current_user, form=form)
