"""
Database entities for use with the backend
Author: Group 7 CSCI 320 01-02
"""
from flask_login import UserMixin
from sqlalchemy.sql import func

from RecipeProject import db
from RecipeProject.Globals import *

# @login_manager.user_loader # Uncomment this function when database is connected
# def load_user(user_email):
#    return User.query.get(user_email)

"""
This is the user, it represents a table. This is not the same as the postgresql table in our remote server
this essentially is a client-side representation of what the server looks like for querying purposes. For each new table
in SQL, you will have have one of these to define it.
"""


class User(db.Model, UserMixin):  # UserMixin tracks user sessions

    __tablename__ = "User"
    email = db.Column(db.String(120), primary_key=True)  # Primary Key

    # Other attributes
    create_datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_access_datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    username = db.Column(db.String(USERNAME_MAX), unique=True, nullable=False)
    password = db.Column(db.String(PASSWORD_SIZE), nullable=False)

    def __repr__(self):
        return f"User {self.username}, Email: {self.email}, Created: {self.create_datetime}"


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
class Recipe(db.Model):
    # Todo Implement (Entity)
    pass


class Pantry(db.model):
    # Todo Implement (Entity)
    pass


class Comprises(db.model):
    # Todo Implement (Relationship)
    pass


class Purchases(db.model):
    # Todo Implement (Relationship)
    pass


class Uses(db.model):
    # Todo Implement (Relationship)
    pass


class Reads(db.model):
    # Todo Implement (Relationship)
    pass


class Creates(db.model):
    # Todo Implement (Relationship)
    pass


class Cooks(db.model):
    # Todo Implement (Relationship)
    pass


class ComprisedOf(db.model):
    # Todo Implement (Relationship)
    pass
"""
