import json
from fractions import Fraction
import pandas as pd
import psycopg2
from sshtunnel import SSHTunnelForwarder

def mixed_to_float(x):
    temp = x.find('-')
    if (temp != -1):
        x = x[:temp]
    return float(sum(Fraction(term) for term in x.split()))

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
        self.tuple_cols = ["Name",
                           "RecipeIngredientQuantities",
                           "RecipeIngredientParts"]

    def add_single_recipe(self, recipe_tuple):
        args = recipe_tuple[8]
        args = args[2:len(args)-1]
        args = args.split(', ')

        args2 = recipe_tuple[7]
        args2 = args2[2:len(args2) - 1]
        args2 = args2.split(', ')
        cursor = self.connection.cursor()

        sql_query = "INSERT INTO ingredient " \
                    "(item_name, quantity_bought, current_quantity, unit_of_measure, purchase_date, expiration_date, pantry_id) " \
            "VALUES (%s, 9999, 9999, 'cups', '2022-10-26', '2023-10-26', 1 )"
        query2 = "SELECT (ingredient_id) FROM ingredient ORDER BY ingredient_id DESC limit 1"
        query3 = "INSERT INTO comprises "\
                 "(quantity, unit, ruid, ingredient_id)" \
                "VALUES (%s, %s, %s, %s)"
        query4 = "SELECT (ruid) FROM recipe WHERE recipe_name = %s"
        try:
            for x in range(len(args)):
                temp = args[x]
                print(temp)
                temp = temp[1:len(temp)-1]
                cursor.execute(sql_query, [temp])
                cursor.execute(query2)
                y = cursor.fetchone()
                #print(y)
                if (len(args2) -1 < x):
                    temp2 = 0
                    unit = "unspecified amount"
                else:
                    temp2 = args2[x]
                    temp2 = temp2[1:len(temp2)-1]
                print(temp2)
                #print(temp2)
                if (temp2 == ''):
                    temp2 = 0
                    unit = "unspecified amount"
                elif (temp2 == 0):
                    temp2 = temp2
                else:
                    unit = "cups"
                    temp2 = mixed_to_float(temp2)

                #need to get ruid
                cursor.execute(query4, [recipe_tuple[1]])
                insert_here = cursor.fetchone()
                temp3 = temp2, unit, insert_here, y
                cursor.execute(query3, temp3)

            self.connection.commit()
            cursor.close()

        except KeyError:
            return
            # cursor.execute(sql_query, args)


    def add_recipes(self, filename: str):

        df = pd.read_csv(filename)

        for index, x in df.iterrows():
            #print(index)
            self.add_single_recipe(x)


di = DataInserter()
di.add_recipes("AlteredRecipes.csv")
