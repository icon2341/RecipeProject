"""
Database entities for use with the backend
Author: Group 7 CSCI 320 01-02
"""
from RecipeProject.Globals import *
from RecipeProject import db
from flask_login import UserMixin

from sqlalchemy.sql import func

#@login_manager.user_loader
#def load_user(user_email):
#    return User.query.get(user_email)


class User(db.Model, UserMixin):
    email = db.Column(db.String(120), primary_key=True)

    create_datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_access_datetime = db.Column(db.Integer)
    username = db.Column(db.String(USERNAME_MAX), unique=True, nullable=False)
    password = db.Column(db.String(PASSWORD_SIZE), nullable=False)

    def __repr__(self):
        return f"User {self.username}, Email: {self.email}, Created: {self.create_datetime}"