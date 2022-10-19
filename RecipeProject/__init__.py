from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# this is a config file, need this for some security crap, not relevant I think, but makes it run happy
app.config['SECRET_KEY'] = '3f07e17a6aca41b3409e6e84af01dfd62ec479a6df127cc58485de51e2488383'


# Demonstration of how to connect to the postgres server
# Todo make this work
username = "group7"
password = "password"
db_name = "db_name"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/{db_name}"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)

from RecipeProject import RecipeBackend
