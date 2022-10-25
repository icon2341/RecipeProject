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
        }

        print("Server is up and running")
        self.connection = psycopg2.connect(**params)

    def get_by(self, table: str, column: str, where: str):
        """
        Returns all instances from the database that match the
        criteria from the parameters
        :param table: Table to query
        :param column: column to check
        :param where: value the column must have to qualify
        :return: Tuple of tuples that are the objects returned
        """
        cursor = self.connection.cursor()
        sql_statement = f"SELECT * FROM \"{table}\" where {column}=\'{where}\';"
        cursor.execute(sql_statement)
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_one_by(self, table: str, column: str, where: str):
        """
        Returns one instance from the database specified by paramaters
        :param table: Table to query
        :param column: Column of that table
        :param where: Value the column should have to qualify
        :return: Full instance of the object returned
        """
        cursor = self.connection.cursor()
        sql_statement = f"SELECT * FROM \"{table}\" where {column}=\'{where}\';"
        cursor.execute(sql_statement)
        result = cursor.fetchone()
        cursor.close()
        return result

    def query(self, query: str, args=()):
        """
        Used for queries that do not return anything from the server
        :param query: SQL Query
        :param args: args to sql query
        :return: Nothing
        """
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        self.connection.commit()
        cursor.close()

    def get_all_query(self, query: str, args=()):
        """
        Executes an sql query and returns all the resulting rows
        :param query: sql query
        :param args: args to the query
        :return: all resulting rows
        """
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall()
        cursor.close()
        return result


    def get_columns(self, table_name: str):
        cursor = self.connection.cursor()
        sql_statement = f'SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{table_name}\'' \
                        f' ORDER BY ordinal_position ASC'
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        cursor.close()
        result = [x[0] for x in result]
        return result


