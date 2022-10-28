"""
THIS FILE IS NOT BEING USED
"""
import datetime

from flask_login import UserMixin

from RecipeProject import login_manager
from RecipeProject import sql


@login_manager.user_loader
def load_user(uuid):
    user = get_user_by_uuid(uuid)
    user.update_access_time()
    return user


"""
This is the user, it represents a table. This is not the same as the postgresql table in our remote server
this essentially is a client-side representation of what the server looks like for querying purposes. For each new table
in SQL, you will have have one of these to define it.
"""


def remove_quotations(string:str):
    return string.replace("\"", "")
def add_ingredient_to_recipe(ruid, ingredient_id, quantity_required, unit):
    sql_query = f"INSERT INTO recipeContains (quantity, unit, ruid, ingredient_id) VALUES ({quantity_required}, {unit}, {ruid}, {ingredient_id})"
    sql.query(sql_query)


def get_pantry(uid):
    pantry = sql.get_all_query(
        f"SELECT i FROM \"User\" INNER JOIN ingredient i on \"User\".pantry_id = i.pantry_id WHERE \"User\".uid={uid}")
    return pantry


def get_nice_columns(table: str):
    """
    Returns the nice printable versions of a table's columns,
    aside from ids. So if a column you want has "id" somewhere in it
    do not use this function
    :param table: Table to get columns from
    :return: Nice and neat column list in ordinal order
    """
    columns = sql.get_columns(table)
    columns = [(x.replace("_", " ")).title() for x in columns if "id" not in x]
    return columns


def get_recipe_if_owned(recipe_id: str, user_id: int):
    if recipe_id.isdigit():
        recipe = Recipe(sql_data=sql.get_one_query(f"SELECT * FROM recipe WHERE ruid={recipe_id} AND uid={user_id}"))
        if recipe.valid():
            return recipe


def get_user_by_uuid(uuid):
    return User(sql_data=sql.get_one_by("User", "uid", uuid))


def get_user_by_username(username):
    return User(sql_data=sql.get_one_by("User", "username", username))


def get_ingredients(ruid):
    ingredients = sql.get_all_query(f"SELECT i.item_name, rC.quantity "
                                    f"FROM recipe "
                                    f"INNER JOIN \"recipeContains\" rC on recipe.ruid = rC.ruid "
                                    f"INNER JOIN ingredient i on rC.ingredient_id = i.ingredient_id "
                                    f"WHERE recipe.ruid={ruid}")

    ingredients = {x[0]: x[1] for x in ingredients}
    return ingredients


class DatabaseObject:
    columns = ["test"]

    def __init__(self, name, sql_data=None, columns=None, **kwargs):
        self.name = name
        if sql_data is not None:
            if columns is not None:
                self.columns = columns
            else:
                self.columns = sql.get_columns(self.name)
            if len(self.columns) == len(sql_data):
                self.data = {}
                for i in range(len(sql_data)):
                    self.data[self.columns[i]] = sql_data[i]
            else:
                raise ValueError("sql_data and columns must be equal length")
        elif kwargs is not None:
            self.data = kwargs
            self.columns = [x for x in self.data.keys()]
        else:
            raise ValueError("Either pass with kwargs or sql_data and columns")

    def valid(self):
        return len(self.data) > 0

    def __getitem__(self, item):
        return self.data[item]
class RecipeContains(DatabaseObject):
    def __init__(self, sql_data=None, columns=None, **kwargs):
        super().__init__("recipeContains", sql_data=sql_data, columns=columns, **kwargs)
class Ingredient(DatabaseObject):

    def __init__(self, sql_data=None, columns=None, **kwargs):
        super().__init__("ingredient", sql_data=sql_data, columns=columns, **kwargs)

    def __str__(self):
        return self["name"]


class Recipe(DatabaseObject):
    columns = []

    def __init__(self, sql_data=None, columns=None, **kwargs):
        super().__init__("recipe", sql_data=sql_data, columns=columns, **kwargs)

        self.data["ingredients"] = get_ingredients(self['ruid'])
        self.data["numberIngredients"] = len(self["ingredients"])

    def make_recipe(self):
        """
        Makes the recipe and changes ingredient quantities in accordance
        :return:
        """
        enough_query = "s"
        enough = sql.get_all_query(enough_query)


class User(UserMixin):  # UserMixin tracks user sessions
    # TODO make username unique in the database
    def __init__(self, sql_data=None, **kwargs):
        if sql_data is not None:
            self.data = {"uuid": sql_data[0], "username": sql_data[1], "email": sql_data[2], "password": sql_data[3],
                         "pantry_id": sql_data[4], "create_datetime": sql_data[5], "last_access": sql_data[6]}

        else:
            self.data = kwargs

    def create_user(self):
        query = f"INSERT INTO \"User\" (username, email, password, create_datetime, last_access )" \
                "VALUES(%s, %s, %s, %s, %s)"
        args = (self['username'], self['email'], self['password'], self['create_datetime'], self['last_access'])

        sql.query(query, args)

        tmp_user = get_user_by_username(self['username'])

        add_pantry_query = f"INSERT INTO pantry (uid) VALUES({tmp_user['uuid']})"
        sql.query(add_pantry_query)

        pantry_id = sql.get_one_by("pantry", "uid", tmp_user['uuid'])[0]

        sql.query(f"UPDATE \"User\" SET pantry_id={pantry_id} WHERE uid={tmp_user['uuid']}")

    def get_id(self):
        return self.data['uuid']

    def valid(self):
        return len(self.data) > 0

    def __getitem__(self, item):
        return self.data[item]

    def update_access_time(self):
        data = (datetime.datetime.now(), self["uuid"])

        sql.query("""UPDATE \"User\" SET last_access=%s WHERE uid=%s""", data)
