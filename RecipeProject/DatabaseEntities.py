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


class DatabaseObject:

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


class Recipe(DatabaseObject):

    def __init__(self, sql_data=None, columns=None, **kwargs):
        super().__init__("recipe", sql_data=sql_data, columns=columns, **kwargs)


class User(UserMixin):  # UserMixin tracks user sessions

    def __init__(self, sql_data=None, **kwargs):

        if sql_data is not None:
            self.data = {
                "uuid": sql_data[0],
                "username": sql_data[1],
                "email": sql_data[2],
                "password": sql_data[3],
                "create_datetime": sql_data[4],
                "last_access": sql_data[5]
            }
        else:
            self.data = kwargs

    def create_user(self):
        query = f"INSERT INTO \"User\" (username, email, password, create_datetime, last_access )" \
                "VALUES(%s, %s, %s, %s, %s)"
        args = (self['username'], self['email'], self['password'], self['create_datetime'], self['last_access'])
        # query = f"INSERT INTO \"User\" (username, email, password, create_datetime, last_access ) \ VALUES('{
        # self.data['uuid']}','{self.data['username']}', '{self.data['email']}', '{self.data['password']}',
        # '{self.data['create_datetime']}', '{self.data['last_access']}');"
        sql.query(query, args)

    def get_id(self):
        return self.data['uuid']

    def valid(self):
        return len(self.data) > 0

    def __getitem__(self, item):
        return self.data[item]

    def update_access_time(self):
        data = (datetime.datetime.now(), self["uuid"])

        sql.query("""UPDATE \"User\" SET last_access=%s WHERE uid=%s""", data)

    """
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)

    # Other attributes
    email = db.Column(db.String(120))  # Primary Key
    create_datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_access_datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    username = db.Column(db.String(USERNAME_MAX), unique=True, nullable=False)
    password = db.Column(db.String(PASSWORD_SIZE), nullable=False)

    def __repr__(self):
        return f"User {self.username}, Email: {self.email}, Created: {self.create_datetime}"
    """


"""
class Ingredient(db.Model):
    __tablename__ = "Ingredient"
    # Was not sure if this should be string or int
    iuid = db.Column(db.Integer, primary_key=True)  # Primary key

    # Other Attributes
    item_name = db.Column(db.String(ITEM_MAX), nullable=False)
    quantity_bought = db.Column(db.Integer, nullable=False)
    current_quantity = db.Column(db.Integer)
    unit = db.Column(db.String(UNIT_MAX))
    purchase_date = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Integer)

    def __repr__(self):
        return f"Ingredient: {self.item_name}, Quantity: {self.current_bought}, Expiration Date: " \
               f"{self.expiration_date}, Unit: {self.unit}"


# Todo Uncomment this block and implement each database entity

"""
