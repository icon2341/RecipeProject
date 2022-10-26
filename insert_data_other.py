import json

import pandas as pd
import psycopg2
from sshtunnel import SSHTunnelForwarder


class DataInserter:

    def __init__(self):
        # Create connection
        with open("PASSWORD.json") as pswd:
            UserData = json.load(pswd)
        db_name = "p32001_07"
        server = SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                    ssh_username=UserData["USERNAME"],
                                    ssh_password=UserData["PASSWORD"],
                                    remote_bind_address=('localhost', 5432))

        server.start()
        params = {
            'dbname': db_name,
            'user': UserData["USERNAME"],
            'password': UserData["PASSWORD"],
            'host': 'localhost',
            'port': server.local_bind_port,
            "keepalives": 2,
            "keepalives_idle": 30,
            "keepalives_interval": 5,
            "keepalives_count": 5
        }

        print("Server is up and running")
        self.connection = psycopg2.connect(**params)
        self.tuple_cols = ["Description",
                           "AggregatedRating",
                           "CookTime",
                           "Name",
                           "RecipeCategory",
                           "RecipeInstructions",
                           "DatePublished",
                           "RecipeServings"]

    def add_single_recipe(self, recipe_tuple):

        cursor = self.connection.cursor()

        sql_query = "INSERT INTO recipe " \
                    "(uid, description, rating, cook_time, recipe_name, category, steps, date_created, servings) " \
                    "VALUES (6, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:

            args = [recipe_tuple[x] for x in self.tuple_cols]

            cursor.execute(sql_query, args)
            self.connection.commit()
            cursor.close()
        except KeyError:
            return
            # cursor.execute(sql_query, args)

    def add_recipes(self, filename: str):

        df = pd.read_csv(filename)

        for index, x in df.iterrows():
            print(index)
            self.add_single_recipe(x)


di = DataInserter()
di.add_recipes("AlteredRecipes.csv")
