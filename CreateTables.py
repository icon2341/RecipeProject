"""
Running this script will mess with tables in the database,
only use it if you have just added new entities to the database
"""

from RecipeProject import conn

with conn.cursor() as cursor:
    query = "CREATE TABLE User (int test)"
    # with open("SQL Code/CreateTable.sql", 'r') as sql_code:

    cursor.execute(query)
