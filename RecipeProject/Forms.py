"""
Form backend for the Recipe project backend
Author: Group 7 CSCI 320 01-02
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# Login form
# Each form shows how the form on the webpage will be set up, and what constraints to put on them
from RecipeProject.Globals import USERNAME_MAX, PASSWORD_MAX


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=2, max=USERNAME_MAX)])  # validators
    # tell you what must happen Ex: Datarequired means you need that bit filled out, length means it must be a certain
    # length
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=PASSWORD_MAX)])
    submit = SubmitField("Log In")  # Submit button


# Registration Form
# same thing as above, but more in depth because the actual registration form, has more steps
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=USERNAME_MAX)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=PASSWORD_MAX)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")