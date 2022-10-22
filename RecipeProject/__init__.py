import json

import psycopg2
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)

# this is a config file, need this for some security crap, not relevant I think, but makes it run happy
app.config['SECRET_KEY'] = '3f07e17a6aca41b3409e6e84af01dfd62ec479a6df127cc58485de51e2488383'

# Demonstration of how to connect to the postgres server
with open("PASSWORD.json") as pswd:
    UserData = json.load(pswd)

username = UserData["USERNAME"]
password = UserData["PASSWORD"]
db_name = "p32001_07"

try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('localhost', 5432)) as server:

        server.start()
        params = {
            'database': db_name,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }
        
        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        bcrypt = Bcrypt(app)
        login_manager = LoginManager(app)
        
        query

        print("Server is up and running")
        from RecipeProject import Routes

except Exception as ex:
    print(ex)
