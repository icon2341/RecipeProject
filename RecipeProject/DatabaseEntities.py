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
Represents the user entity in the database
"""


class User(db.Model, UserMixin):  # UserMixin tracks user sessions

    __tablename__ = "User"
    email = db.Column(db.String(120), primary_key=True)  # Primary Key

    # Other attributes
    create_datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_access_datetime = db.Column(db.Integer)
    username = db.Column(db.String(USERNAME_MAX), unique=True, nullable=False)
    password = db.Column(db.String(PASSWORD_SIZE), nullable=False)

    def __repr__(self):
        return f"User {self.username}, Email: {self.email}, Created: {self.create_datetime}"


# Todo Uncomment this block and implement each database entity

"""
class Ingredient(db.Model):
    # Todo Implement (Entity)
    pass


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
