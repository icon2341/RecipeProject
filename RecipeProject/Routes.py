"""
Flask Backend to the recipe project web interface
Author: Group 7 CSCI 320 01-02
"""
import datetime

from flask import render_template, request, redirect
from flask_login import login_user, login_required, logout_user, current_user
from RecipeProject import sql
from RecipeProject import app, bcrypt, login_manager
from RecipeProject.DatabaseEntities import get_user_by_username, User, Recipe, get_recipe_if_owned, get_pantry, \
    get_ingredients
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
    pantry = get_pantry(current_user['uuid'])
    print(pantry)
    for y in range(len(pantry)):
        x = pantry[y]
        x = x[0]
        x = x[1:len(x)-1]
        x = x.split(',')
        pantry[y] = {"item_name" : x[7],
                     "quantity_bought": x[0],
                     "current_quantity": x[1],
                     "purchase_date": x[3],
                     "expiration_date": x[4],
                     "unit_of_measure": x[5]
                     }

    return render_template("Pantry.html", user=current_user, pantry=pantry, form=form)

    '''
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
'''

@app.route("/MyRecipes")
@login_required
def myRecipes():
    limit = 50  # Limit of the number of recipes returned
    # TODO JOIN table with ingredients
    recipes = [Recipe(sql_data=data) for data in
               sql.get_all_query(f"SELECT * FROM recipe WHERE uid={current_user['uuid']} LIMIT {limit}")]

    return render_template("MyRecipes.html", user=current_user, recipes=recipes)


@app.route("/Home")
@login_required
def Home():
    return render_template("Home.html", user=current_user)


@app.route("/NewIngredient", methods=["GET", "POST"])
@login_required
def NewIngredient():
    form = IngredientEditing()

    # if request.method == "GET":

    if request.method == "POST":
        sql_query = "INSERT INTO ingredient (expiration_date, purchase_date, quantity_bought," \
                    " units_of_measure, item_name, quantity_bought, pantry_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        args = (
            form.expiration.data,
            form.purchase.data,
            form.quantity.data,
            form.units.data,
            form.name.data,
            form.bought.data,
            current_user["pantry_id"]
        )

        sql.query(sql_query, args)
        print(current_user["pantry_id"])
        return redirect("/Pantry")

    return render_template("NewIngredient.html", user=current_user, form=form)


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
    # TODO do stuff with
    form = RecipeEditing()
    if request.method == "GET":

        return render_template("NewRecipe.html", user=current_user, form=form)
    elif request.method == "POST":
        sql_query = f"INSERT INTO recipe (servings, recipe_name, difficulty, cook_time," \
                    f" category, steps, description, rating, uid, date_created) " \
                    f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        args = (
            form.servings.data,
            form.title.data,
            form.difficulty.data,
            form.prep_time.data,
            form.category.data,
            form.steps.data,
            form.description.data,
            form.rating.data,
            current_user["uuid"],
            datetime.datetime.now()
        )
        sql.query(sql_query, args)
        return redirect("/MyRecipes")


@app.route("/EditIngredientQuantities", methods=["GET", "POST"])
@login_required
def EditIngredientQuantities():
    ingredients = {"Tomato": "4", "Baby": "3", "Crow": "6"}

    if request.method == "POST":
        for i in ingredients.keys():
            print(i)
            print(request.form.get(i))

        return render_template("editIngredientQuantity.html", user=current_user, ingredients=ingredients)
    elif request.method == "GET":
        return render_template("editIngredientQuantity.html", user=current_user, ingredients=ingredients)


@app.route("/editRecipe", methods=["GET", "POST"])
@login_required
def EditRecipe():
    # TODO Do stuff with ingredients
    form = RecipeEditing()
    # requests recipe ID for passing onto system and later usage. 

    recipe_id = request.args.get("rId")
    if request.method == "GET":
        recipe = get_recipe_if_owned(recipe_id, current_user["uuid"])
        # re populate fields
        if recipe is not None:
            form.servings.data = float(recipe["servings"])
            form.title.data = recipe["recipe_name"]
            form.difficulty.data = recipe["difficulty"]
            form.prep_time.data = recipe["cook_time"]
            form.category.data = recipe['category']
            form.steps.data = recipe['steps']
            form.description.data = recipe['description']
            form.rating.data = recipe['rating']
            ingredients_checked = get_ingredients(recipe['ruid'])

            return render_template("EditRecipe.html", user=current_user, form=form,
                                   ingredients_checked=ingredients_checked,
                                   ingredients=get_pantry(current_user["uuid"]))
        # Non valid recipe id
        else:
            return redirect("/MyRecipes")
        # submission
    elif request.method == "POST":
        sql_query = f"UPDATE recipe " \
                    f"SET servings=%s, " \
                    f"recipe_name=%s, " \
                    f"difficulty=%s, " \
                    f"cook_time=%s, " \
                    f"category=%s, " \
                    f"steps=%s, " \
                    f"description=%s, " \
                    f"rating=%s" \
                    f"WHERE ruid=%s"

        # query args, use %s and these OR use fstrings and manually pass in.
        args = (
            form.servings.data,
            form.title.data,
            form.difficulty.data,
            form.prep_time.data,
            form.category.data,
            form.steps.data,
            form.description.data,
            form.rating.data,
            recipe_id
        )

        ingredients = request.form.getlist('ingredients')
        #query executer
        sql.query(sql_query, args)

        # return render_template("EditRecipe.html", user=current_user, form=form)
        return redirect("/EditIngredientQuantities")
'''
@app.route('/IngredientSearch', methods=["POST"])
@login_required
def ingredientSearch():
    form = ingredientSearch()
    if form.validate_on_submit():
        args = form.searchField.data'''

