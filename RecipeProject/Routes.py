"""
Flask Backend to the recipe project web interface
Author: Group 7 CSCI 320 01-02
"""
import datetime
import json

from flask import render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from RecipeProject import sql
from RecipeProject import app, bcrypt, login_manager
from RecipeProject.DatabaseEntities import get_user_by_username, User, Recipe, get_recipe_if_owned, get_pantry, \
    get_ingredients, Ingredient, RecipeContains, remove_quotations
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


@app.route("/Pantry", methods=["GET", "POST"])
@login_required
def Pantry():
    form = IngredientSearch()

    if request.method == "GET":
        pantry = get_pantry(current_user['uuid'])
        ingreds = [Ingredient(sql_data=x) for x in pantry]
        return render_template("Pantry.html", user=current_user, pantry=ingreds, form=form)

    elif request.method == "POST":

        pantry = sql.get_filtered_pantry(current_user['uuid'], form.sortBy.data, form.order.data, form.searchField.data)

        ingreds = [Ingredient(sql_data=x) for x in pantry]

        print([x.data for x in ingreds])
        print(request.data)
        for ingredient in ingreds:
            # print(request.form[ingredient['ingredient_id']])
            if ingredient['current_quantity'] != request.form.get(ingredient['ingredient_id']):
                print(request.form.get(ingredient['ingredient_id']))
        """
        for y in range(len(pantry)):
            x = pantry[y]
            x = x[0]
            x = x[1:len(x) - 1]
            x = x.split(',')
            pantry[y] = {"item_name": x[7],
                         "quantity_bought": x[0],
                         "current_quantity": x[1],
                         "purchase_date": x[3],
                         "expiration_date": x[4],
                         "unit_of_measure": x[2]
                         }
        """
        # if request.form.get(pantry[y]['item_name'])
        return render_template("Pantry.html", user=current_user, pantry=ingreds, form=form)


@app.route("/MyRecipes")
@login_required
def myRecipes():
    limit = 50  # Limit of the number of recipes returned
    # TODO JOIN table with ingredients
    recipes = [Recipe(sql_data=data) for data in
               sql.get_all_query(f"SELECT * FROM recipe WHERE uid={current_user['uuid']} LIMIT {limit}")]

    return render_template("MyRecipes.html", user=current_user, recipes=recipes)


@app.route("/Home", methods=["GET", "POST"])
@login_required
def Home():
    form = RecipeSearch()
    if request.method == "GET":
        recipes = [Recipe(sql_data=data) for data in
                   sql.get_all_query(f"SELECT * FROM recipe LIMIT {50}")]
        return render_template("Home.html", user=current_user, recipes=recipes, form=form)
    elif request.method == "POST":

        recipes_data = sql.get_filtered_recipe(form.sortBy.data, form.order.data, form.nameSearch.data,
                                               form.ingredientSearch.data, form.categorySearch.data)
        recipes = []
        for recipe in recipes_data:
            recipes.append(Recipe(sql_data=recipe))

        return render_template("Home.html", user=current_user, recipes=recipes, form=form)


@app.route("/NewIngredient", methods=["GET", "POST"])
@login_required
def NewIngredient():
    form = IngredientEditing()

    # if request.method == "GET":

    if request.method == "POST":
        sql_query = "INSERT INTO ingredient (expiration_date, purchase_date, current_quantity," \
                    " unit_of_measure, item_name, quantity_bought, pantry_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"

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
    form = RecipeEditing()

    if request.method == "GET":
        """
        ingredients = []
        for ingredient in get_pantry(current_user['uuid']):
            ingredient = ingredient[0][1:-1]
            ingredients.append(Ingredient(sql_data=ingredient.split(",")))
        """

        return render_template("newRecipe.html", user=current_user, form=form)
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

        """

        ingredients = request.form.getlist('ingredients')
        for ingredient in ingredients:

            recipe_contains_data = sql.get_one_by("recipeContains", "ingredient_id", ingredient)
            if not recipe_contains_data:
                ingredientEntity = Ingredient(sql_data=sql.get_one_by("ingredient", "ingredient_id", ingredient))
                measure = ingredientEntity["unit_of_measure"]
                quantity = 0
            else:
                recipe_contains = RecipeContains(sql_data=recipe_contains_data)
                measure = recipe_contains['unit']
                quantity = recipe_contains['quantity']
            # Check if the item is already in the recipe

            add_query = f"INSERT INTO \"recipeContains\" (quantity, unit, ruid, ingredient_id) VALUES (%s, %s, %s, %s)"
            add_args = (quantity, measure, recipe_id, ingredient)

            sql.query(add_query, add_args)
"""
        # return render_template("EditRecipe.html", user=current_user, form=form)
        return redirect("/EditIngredientQuantities")


@app.route("/EditIngredientQuantities", methods=["GET", "POST"])
@login_required
def EditIngredientQuantities():
    recipe_id = request.args.get("rId")
    if not recipe_id:
        return redirect("/MyRecipes")
    ingredients = sql.get_all_query(
        f"SELECT i.item_name, rC.quantity FROM \"recipeContains\" rC INNER JOIN ingredient i on i.ingredient_id = rC.ingredient_id where rC.ruid={recipe_id};")
    ingredients = {x[0].title(): x[1] for x in ingredients}

    if request.method == "POST":
        for i in ingredients.keys():
            sql_query = f"UPDATE \"recipeContains\" as r " \
                        f"SET quantity = {request.form.get(i)} " \
                        f"FROM ingredient as i " \
                        f"WHERE i.ingredient_id = r.ingredient_id and i.item_name LIKE \'%{i.lower()}%\' and r.ruid = {recipe_id};"

            # will need to update based on inner join with ingredients and recipeContain
            sql.query(sql_query)
        return redirect("/MyRecipes")
    elif request.method == "GET":

        return render_template("editIngredientQuantity.html", user=current_user, ingredients=ingredients)


@app.route("/editRecipe", methods=["GET", "POST"])
@login_required
def EditRecipe():

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
            ingredients = []
            for ingredient in get_pantry(current_user['uuid']):
                ingredients.append(Ingredient(sql_data=ingredient))

            return render_template("EditRecipe.html", user=current_user, form=form,
                                   ingredients_checked=ingredients_checked,
                                   ingredients=ingredients)
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
        sql.query(sql_query, args)

        delete_query = f"DELETE FROM \"recipeContains\" WHERE \"recipeContains\".ruid = {recipe_id} "

        sql.query(delete_query)

        ingredients = request.form.getlist('ingredients')
        for ingredient in ingredients:

            recipe_contains_data = sql.get_one_by("recipeContains", "ingredient_id", ingredient)
            if not recipe_contains_data:
                ingredientEntity = Ingredient(sql_data=sql.get_one_by("ingredient", "ingredient_id", ingredient))
                measure = ingredientEntity["unit_of_measure"]
                quantity = 0
            else:
                recipe_contains = RecipeContains(sql_data=recipe_contains_data)
                measure = recipe_contains['unit']
                quantity = recipe_contains['quantity']
            # Check if the item is already in the recipe

            add_query = f"INSERT INTO \"recipeContains\" (quantity, unit, ruid, ingredient_id) VALUES (%s, %s, %s, %s)"
            add_args = (quantity, measure, recipe_id, ingredient)

            sql.query(add_query, add_args)

        # return render_template("EditRecipe.html", user=current_user, form=form)
        return redirect("/EditIngredientQuantities")


@app.route("/cookRecipe", methods=["GET", "POST"])
@login_required
def cookRecipe():
    recipeId = request.args.get("rId")
    scalar = float(request.args.get("multiplier"))
    rating = int(request.args.get('ratingPassed'))

    if request.method == "GET":
        if recipeId is None:
            print("recipe id was none, cant cook")
            return redirect("/Home")

        # we will need to get the id for the recipe that we are trying to cook
        # we will use this ID to determine recipe requirments/quantites

        # then need to get the ingredients/quantites that the user OWNS that are ALSO in the recipe
        # if the lists are not equal OR the quantities are not greater or equal then we will FAIL and redirect the user
        # back to home and tell them to add the ingredients to their pantry.
        get_recipe_req_query = \
            f"SELECT i.item_name, rC.quantity FROM recipe " \
            f"INNER JOIN \"recipeContains\" rC on recipe.ruid = rC.ruid " \
            f"INNER JOIN ingredient i on i.ingredient_id = rC.ingredient_id " \
            f"WHERE recipe.ruid={recipeId};"

        recipe_quantities = sql.get_all_query(get_recipe_req_query)

        # get_user_recipe_ingredients_intersection = f"SELECT i.item_name, i.current_quantity FROM pantry " \ f"INNER
        # JOIN ingredient i on pantry.pantry_id = i.pantry_id " \ f"INNER JOIN \"recipeContains\" rC on
        # i.ingredient_id = rC.ingredient_id " \ f"WHERE pantry.uid = {current_user['uuid']} and rC.ruid = {recipeId} "

        get_user_recipe_ingredients_intersection2 = f"SELECT i.item_name, i.current_quantity FROM ingredient i " \
                                                    f"INNER JOIN pantry on i.pantry_id = pantry.pantry_id " \
                                                    f"WHERE pantry.uid = {current_user['uuid']}"

        user_quantities = sql.get_all_query(get_user_recipe_ingredients_intersection2)

        # get ingredient names in user quantities
        userIngredientQuantities = set()
        for ingredientTuple in user_quantities:
            userIngredientQuantities.add(ingredientTuple[0])

        recipeIngredienQuantities = set()
        for ingredientTuple in recipe_quantities:
            recipeIngredienQuantities.add(ingredientTuple[0])

        print(recipe_quantities, user_quantities)
        print(userIngredientQuantities, recipeIngredienQuantities)
        if recipeIngredienQuantities.issubset(userIngredientQuantities):

            recipe_quantities = {x[0]: x[1] for x in recipe_quantities}
            user_quantities = {remove_quotations(x[0]): x[1] for x in user_quantities}

            # Sends the user to the home page if they dont have enough ingredients for the thing0
            for key in recipe_quantities.keys():
                if recipe_quantities[key] > user_quantities[key]:
                    return redirect("/Home")

            for key in recipe_quantities.keys():
                new_quant = user_quantities[key] - recipe_quantities[key] * scalar

                update_query = f"UPDATE ingredient as i SET current_quantity={new_quant} FROM pantry as p " \
                               f"WHERE p.uid = {current_user['uuid']} AND p.pantry_id = i.pantry_id AND i.item_name = \'{key}\'"
                sql.query(update_query)

            recipe = Recipe(sql_data=sql.get_one_by("recipe", "ruid", recipeId))

            insert_cook = f"INSERT INTO cooks (uid, ruid, date_made, quantity_made, portions_made, user_rating) Values ({current_user['uuid']}," \
                          f" {recipeId},\'{datetime.datetime.now()}\', " \
                          f"{scalar * float(recipe['servings'])}, " \
                          f"{scalar}" \
                          f", {rating})"

            sql.query(insert_cook)

        else:
            print("User does not have the ingredients to cook this recipe")
            return redirect("/Home")

        # User can do stuff
        flash('You were successfully logged in')
        return redirect("/Home")


@app.route("/deleteRecipe", methods=["GET"])
@login_required
def deleteRecipe():
    recipeId = request.args.get("rId")
    if request.method == "GET":
        # if a user has cooked this recipe, then deletion fail, do nothing
        # if green, then delete the recipe, and the recipeContains entry
        check_cooked_query = f'SELECT * FROM cooks where ruid={recipeId}'
        recipeCooks = sql.get_all_query(check_cooked_query)
        print(recipeCooks)

        if not recipeCooks:
            # query returned nothing, run query
            delete_rc_query = f'DELETE FROM "recipeContains" WHERE "recipeContains".ruid ={recipeId} '
            delete_recipe_query = f'DELETE FROM recipe WHERE recipe.ruid={recipeId}'
            sql.query(delete_rc_query)
            sql.query(delete_recipe_query)
        else:
            print("cant delete")

    return redirect("/MyRecipes")
    '''
@app.route('/IngredientSearch', methods=["POST"])
@login_required
def ingredientSearch():
    form = ingredientSearch()
    if form.validate_on_submit():
        args = form.searchField.data'''


@app.route("/cookedRecipes", methods=["GET"])
@login_required
def cookedRecipes():
    uid = current_user['uuid']
    if request.method == "GET":
        get_cooked_query = f'SELECT r.* FROM cooks INNER JOIN recipe r on r.ruid = cooks.ruid WHERE cooks.uid={uid}'

        recipe_data = sql.get_all_query(get_cooked_query)
        foodCooked = []

        for x in recipe_data:
            new_recipe = Recipe(sql_data=x)
            get_cooked_time_query = f'SELECT date_made FROM cooks where ruid={new_recipe["ruid"]}'
            new_recipe.data['cooked_last'] = sql.get_one_query(get_cooked_time_query)[0]
            foodCooked.append(new_recipe)

        # if recipe_data is not None:
        # foodCooked = [Recipe(sql_data=x) for x in recipe_data]

        return render_template("cookedRecipes.html", user=current_user, recipes=foodCooked)


@app.route("/editIngredientQuantity", methods=["GET"])
@login_required
def change_ingredient_quantity():
    ingredient = request.args.get("iId")
    new_quantity = request.args.get("newQuantity")

    if ingredient is None or new_quantity is None:
        print("ERROR")

    sql_query = f"UPDATE ingredient SET current_quantity={new_quantity} WHERE ingredient_id={ingredient}"
    sql.query(sql_query
              )
    return redirect("/Pantry")


@app.route("/TopFifty")
@login_required
def myTopFifty():
    limit = 50  # Limit of the number of recipes returned
    query = f"""SELECT recipe.*, CASE WHEN cookrat.avg_rating IS NULL THEN recipe.rating ELSE cookrat.avg_rating END as rat
FROM recipe FULL JOIN 
    (SELECT AVG(user_rating) as avg_rating, ruid FROM cooks GROUP BY ruid) 
        as cookrat ON cookrat.ruid=recipe.ruid
     ORDER BY rat DESC LIMIT {limit}"""
    recipes = [Recipe(sql_data=data) for data in sql.get_all_query(query)]
    return render_template("TopFifty.html", user=current_user, recipes=recipes)


@app.route("/RecentlyCreated")
@login_required
def RecentlyCreatedRecipes():
    limit = 50  # Limit of the number of recipes returned
    recipes = [Recipe(sql_data=data) for data in

               sql.get_all_query(f"SELECT * FROM recipe ORDER BY recipe.date_created DESC LIMIT {limit}")]
    return render_template("RecentlyCreated.html", user=current_user, recipes=recipes)


@app.route("/InPantry")
@login_required
def InPantry():
    limit = 50  # Limit of the number of recipes returned
    in_pantry_query = f"""
    SELECT recipe.*, CASE WHEN cookrat.avg_rating IS NULL THEN recipe.rating ELSE cookrat.avg_rating END as avg_rating
FROM (SELECT recipe.* FROM recipe
INNER JOIN
(SELECT MIN(conditional_table.ValidIngredient) as valid_recipe, conditional_table.ruid FROM
(SELECT
    CASE WHEN (user_ingredients.current_quantity IS NOT NULL AND recipe_ingredient.quantity <= user_ingredients.current_quantity) THEN 1 ELSE 0 END AS ValidIngredient,
    recipe_ingredient.quantity,
    recipe_ingredient.ruid,
    recipe_ingredient.recipe_name,
    recipe_ingredient.item_name,
    user_ingredients.current_quantity
    FROM
    (SELECT i.item_name, rC.quantity, recipe.ruid, recipe_name FROM recipe
    INNER JOIN "recipeContains" rC on recipe.ruid = rC.ruid
    INNER JOIN ingredient i on i.ingredient_id = rC.ingredient_id) as recipe_ingredient
    FULL JOIN (SELECT i2.item_name, i2.current_quantity FROM "User"
                         INNER JOIN pantry p on "User".pantry_id = p.pantry_id
                         INNER JOIN ingredient i2 on p.pantry_id = i2.pantry_id
                         WHERE "User".uid={current_user['uuid']}) as user_ingredients
    ON user_ingredients.item_name=recipe_ingredient.item_name) as conditional_table
GROUP BY ruid) as makeable_recipes

ON recipe.ruid=makeable_recipes.ruid
WHERE makeable_recipes.valid_recipe=1
ORDER BY recipe.rating DESC) as recipe FULL JOIN
    (SELECT AVG(user_rating) as avg_rating, ruid FROM cooks GROUP BY ruid)
        as cookrat ON cookrat.ruid=recipe.ruid
     WHERE recipe.ruid IS NOT NULL
     ORDER BY avg_rating DESC
    LIMIT {limit};
    """

    recipe_data = sql.get_all_query(in_pantry_query)
    recipes = [Recipe(sql_data=data) for data in recipe_data]

    return render_template("InPantry.html", user=current_user, recipes=recipes)


@app.route("/Recommended")
@login_required
def Recommended():
    limit = 50  # Limit of the number of recipes returned

    query = f"""
    SELECT DISTINCT recipe.*, CASE WHEN cookrat.avg_rating IS NULL THEN recipe.rating ELSE cookrat.avg_rating END as avg_rating
FROM (SELECT r2.* FROM recipe as r2 INNER JOIN (
SELECT cooks.ruid FROM cooks INNER JOIN (
SELECT DISTINCT c1.ruid, c2.uid
      FROM cooks as c1
               FULL JOIN cooks as c2 on c1.ruid = c2.ruid
        WHERE c1.uid = {current_user['uuid']} AND c2.uid != c1.uid) as common
        ON cooks.uid = common.uid
        WHERE cooks.ruid != common.ruid) as rec_recipe ON r2.ruid=rec_recipe.ruid) as recipe FULL JOIN
    (SELECT AVG(user_rating) as avg_rating, ruid FROM cooks GROUP BY ruid)
        as cookrat ON cookrat.ruid=recipe.ruid
    WHERE recipe.ruid IS NOT NULL
     ORDER BY avg_rating DESC
     LIMIT {limit}
    """

    query_result = sql.get_all_query(query)
    recipes = [Recipe(sql_data=data) for data in query_result]
    return render_template("InPantry.html", user=current_user, recipes=recipes)
