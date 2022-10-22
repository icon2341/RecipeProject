import json

import psycopg2
from sshtunnel import SSHTunnelForwarder


def sql_query(query):
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
                'dbname': db_name,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port,
                "keepalives": 2,
                "keepalives_idle": 30,
                "keepalives_interval": 5,
                "keepalives_count": 5
            }
            print("Server is up and running")

            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()


    except Exception as ex:
        print(ex)

def get_one(query):
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
                'dbname': db_name,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port,
                "keepalives": 2,
                "keepalives_idle": 30,
                "keepalives_interval": 5,
                "keepalives_count": 5
            }
            print("Server is up and running")

            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            return result


    except Exception as ex:
        print(ex)

def return_query(query):
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
                'dbname': db_name,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port,
                "keepalives": 2,
                "keepalives_idle": 30,
                "keepalives_interval": 5,
                "keepalives_count": 5
            }
            print("Server is up and running")

            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            return result

    except Exception as ex:
        print(ex)

