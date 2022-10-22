"""
THIS FILE IS NOT BEING USED
this file is an SQL alchemy based
"""
from flask_login import UserMixin
from RecipeProject import login_manager
from RecipeProject.Globals import *
from RecipeProject.SQLInterface import sql_query, get_one


@login_manager.user_loader  # Uncomment this function when database is connected
def load_user(uuid):
    return get_user_by_uuid(uuid)


#    print(f"Logging in: {email}")
#    return User.query.get(email)


"""
This is the user, it represents a table. This is not the same as the postgresql table in our remote server
this essentially is a client-side representation of what the server looks like for querying purposes. For each new table
in SQL, you will have have one of these to define it.
"""


def get_user_by_uuid(uuid):
    return User(sql_data=get_one(f"SELECT * FROM \"User\" where uid=\'{uuid}\'"))


def get_user_by_username(username):
    return User(sql_data=get_one(f"SELECT * FROM \"User\" where username=\'{username}\'"))


class User(UserMixin):  # UserMixin tracks user sessions

    def __init__(self, sql_data=None, **kwargs):

        if sql_data is not None:
            self.data = {}
            self.data["uuid"] = sql_data[0]
            self.data["username"] = sql_data[1]
            self.data["email"] = sql_data[2]
            self.data["password"] = sql_data[3]
            self.data["create_datetime"] = sql_data[4]
            self.data["last_access"] = sql_data[5]
        else:
            self.data = kwargs

    def create_user(self):
        query = f"INSERT INTO \"User\" (uid, username, email, password, create_datetime, last_access ) \
            VALUES('{self.data['uuid']}','{self.data['username']}', '{self.data['email']}', '{self.data['password']}', '{self.data['create_datetime']}', '{self.data['last_access']}');"
        print(query)
        sql_query(query)

    def get_id(self):
        return self.data['uuid']

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
