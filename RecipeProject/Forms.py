"""
Form backend for the Recipe project backend
Author: Group 7 CSCI 320 01-02
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from RecipeProject import bcrypt
from RecipeProject.Globals import USERNAME_MAX, PASSWORD_MAX


# Login form
# Each form shows how the form on the webpage will be set up, and what constraints to put on them
class LoginForm(FlaskForm):
    # Validators tell you what must happen Ex: Datarequired means you need that bit filled out, length means it must
    # be a certain length
    username = StringField('Username:', validators=[DataRequired(), Length(min=2, max=USERNAME_MAX)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=PASSWORD_MAX)])
    # Submit button
    submit = SubmitField("Log In")


# Registration Form
# same thing as above, but more in depth because the actual registration form, has more steps
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=USERNAME_MAX)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=PASSWORD_MAX)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField("Sign Up")

class ResetPassword(FlaskForm):

    password = StringField("Current Password", validators=[DataRequired()])
    new_password = StringField("New Password", validators=[DataRequired()])
    confirm_password = StringField("Confirm New Password", validators=[DataRequired(), EqualTo("New Password")])
    submit = SubmitField("Submit")

    def validate_password(self, password):
        if bcrypt.check_password_hash(current_user['password'], password.data):
            return True
        raise ValidationError("Incorrect Password")

"""
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            print("USERNAME IS TAKEN")
            raise ValidationError("USERNAME IS TAKEN")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            print("EMAIL IS TAKEN")
            raise ValidationError("EMAIL IS TAKEN")
"""
