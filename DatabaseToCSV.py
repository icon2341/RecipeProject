"""
Script for taking the database data and putting it into a folder full of csv's.
Each csv will represent one table in the database
"""
import json
import os

import pandas as pd
import psycopg2
from sshtunnel import SSHTunnelForwarder


def connect():
    """
    Returns a database connection
    :return: Database connection
    """
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
    }

    return psycopg2.connect(**params)

def get_tables(connection):
    """
    Gets a list of tables from the database
    :param connection: SQL Connection
    :return: List of tables in the database
    """

    cursor = connection.cursor()

    cursor.execute("SELECT table_name FROM information_schema.tables where table_schema='p32001_07'")

    result = cursor.fetchall()

    cursor.close()

    return result

if __name__ == "__main__":

    con = connect()
    tables = get_tables(con)

    folder_name = "TableCSV"
    try:
        os.mkdir(folder_name)
    except OSError as error:
        print(error)

    tables = [x[0] for x in tables]
    for table in tables:
        query = f"SELECT * FROM \"{table}\";"
        df = pd.read_sql(query, con)

        df.to_csv(folder_name + f"/{table}.csv")

        print(f"Table {table} read to csv")
