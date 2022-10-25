'''
This program parses through data from a file and puts in into the database
'''
import pandas as pd
import isodate
import psycopg2
import json
from sshtunnel import SSHTunnelForwarder
host_name = host='starbug.cs.rit.edu'
dbname="p32001_07"
port = 5432
def __init__():
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
        connection = psycopg2.connect(**params)
        return connection

def exists(curr, ruid):
    query = ("""Select ruid FROM recipe WHERE ruid = %s""")
    curr.execute(query, [ruid])
    return curr.fetchone() is not None

def update_row(curr, servings, description,
               rating, cook_time, ruid,
               recipe_name, category, steps, date_created):
    cook_time = (isodate.parse_duration(cook_time))
    query = ("""UPDATE recipe SET servings = %s,
    description = %s, rating = %s , cook_time = %s , 
    recipe_name = %s , category = %s, steps = %s, difficulty = 0, date_created = %s""")
    vars = (servings, description, rating, cook_time,
            recipe_name, category, steps, date_created)
    curr.execute(query, vars)


def update_db(curr, df):
    tmp_df = pd.DataFrame(columns=['servings',  'description',
                          'rating', 'cook_time', 'ruid',
                                   'recipe_name', 'category', 'steps',
                                   'date_created'])
    for i, row in df.iterrows():
        if exists(curr, row['ruid']):
            update_row(curr, row['servings'], row['description'],
                       row['rating'], row['cook_time'], row['ruid'],
                       row['recipe_name'], row['category'], row['steps'], row['date_created'])
        else:
            tmp_df = tmp_df.append(row)
    return tmp_df

def insert_into_table(curr, servings,  description,
                          rating, cook_time, ruid,
                                   recipe_name, category, steps, date_created):
    cook_time = (isodate.parse_duration(cook_time))
    query = ("""INSERT INTO recipe (servings,  description,
                          rating, cook_time, ruid,
                                   recipe_name, category, steps, difficulty, date_created, uid)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 0, %s, 6);""")
    row = servings, description,rating, cook_time, ruid, recipe_name, category, steps, date_created
    curr.execute(query, row)

def insert(curr, df):
    for i, row in df.iterrows():
        insert_into_table(curr, row['servings'], row['description'],
                          row['rating'], row['cook_time'], row['ruid'],
                                   row['recipe_name'], row['category'], row['steps'], row['date_created'])
con = __init__()
curr = con.cursor()
df = pd.read_csv('recipes.csv', usecols=['servings', 'description',
                          'rating', 'cook_time', 'ruid',
                                   'recipe_name', 'category', 'steps', 'date_created'], nrows=23) #remove nrows to parse all data
tmp_df = update_db(curr, df)
insert(curr, tmp_df)
con.commit()
print("Data added")
#row 24 makes it break