from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from RecipeProject.SQLInterface import SQLInterface

app = Flask(__name__)

# this is a config file, need this for some security crap, not relevant I think, but makes it run happy
app.config['SECRET_KEY'] = '3f07e17a6aca41b3409e6e84af01dfd62ec479a6df127cc58485de51e2488383'

# Demonstration of how to connect to the postgres server
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
sql = SQLInterface()
from RecipeProject import Routes
