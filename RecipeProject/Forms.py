"""
Form backend for the Recipe project backend
Author: Group 7 CSCI 320 01-02
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, SelectField, RadioField, DateTimeField, \
    IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea

from RecipeProject import bcrypt, sql
from RecipeProject.DatabaseEntities import get_nice_columns
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
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")


class ResetPassword(FlaskForm):
    password = StringField("Current Password", validators=[DataRequired()])
    new_password = StringField("New Password", validators=[DataRequired()])
    confirm_password = StringField("Confirm New Password", validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Submit")

    def validate_password(self, password):
        if bcrypt.check_password_hash(current_user['password'], password.data):
            return True
        raise ValidationError("Incorrect Password")


class IngredientSearch(FlaskForm):
    order = RadioField("AscDesc", choices=["Ascending", "Descending"])
    searchField = StringField("SearchField")
    sortBy = SelectField("Sort By", choices=get_nice_columns("ingredient"))
    submit = SubmitField("SearchButton")


class RecipeEditing(FlaskForm):
    title = StringField("Title")
    servings = DecimalField("Servings")
    difficulty = IntegerField("Difficulty")
    rating = IntegerField("Rating")
    possible_categories = [x[0] for x in sql.get_all_query(f"SELECT DISTINCT category FROM recipe")]
    category = SelectField("Category", choices=possible_categories)
    prep_time = DateTimeField("Preparation Time", format="%H:%M")
    description = StringField("Description", widget=TextArea())
    steps = StringField("Steps", widget=TextArea())
    submit = SubmitField("Submit")


class IngredientEditing(FlaskForm):
    expiration = DateTimeField("Expiration Date")
    purchase = DateTimeField("Purchase Date", validators=[DataRequired()])
    quantity = DecimalField("Quantity")
    units = StringField("Units")
    name = StringField("Name", validators=[DataRequired()])
    bought = DecimalField("Quantity Bought", validators=[DataRequired()])
    submit = SubmitField("Submit")
