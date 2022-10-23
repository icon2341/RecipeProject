import json

import psycopg2
from sshtunnel import SSHTunnelForwarder


class SQLInterface:

    def __init__(self):
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

    def get_by(self, table: str, column: str, where: str):
        cursor = self.connection.cursor()
        sql_statement = f"SELECT * FROM \"{table}\" where {column}=\'{where}\';"
        cursor.execute(sql_statement)
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_one_by(self, table: str, column: str, where: str):
        cursor = self.connection.cursor()
        sql_statement = f"SELECT * FROM \"{table}\" where {column}=\'{where}\';"
        cursor.execute(sql_statement)
        result = cursor.fetchone()
        cursor.close()
        return result

    def query(self, query: str, args=()):
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        self.connection.commit()
        cursor.close()

    def get_columns(self, table_name: str):
        cursor = self.connection.cursor()
        sql_statement = f'SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE %s = N\'Customers\''
        cursor.execute(sql_statement, (table_name))
        result = cursor.fetchall()
        cursor.close()
        return result


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
