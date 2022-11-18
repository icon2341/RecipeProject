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

        self.connection = psycopg2.connect(**params)
        print("Server is up and running")

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
        if not args:
            cursor.execute(query)
        else:
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

    def get_one_query(self, query: str, args=()):
        """
        Executes an sql query and returns all the resulting rows
        :param query: sql query
        :param args: args to the query
        :return: all resulting rows
        """
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        result = cursor.fetchone()
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

    def get_filtered_pantry(self, uid, order_by, order, search_value):
        if order == "Ascending":
            order = "ASC"
        elif order == "Descending":
            order = "DESC"
        else:
            order="ASC"

        if not order_by:
            order_by = "item_name"
        contains_clause = ""
        if search_value is not None:
            contains_clause = f" AND i.item_name LIKE '%{search_value}%' "

        query = f"SELECT i.* FROM \"User\" " \
                f"INNER JOIN ingredient i on \"User\".pantry_id = i.pantry_id " \
                f"WHERE \"User\".uid={uid} {contains_clause}" \
                f"ORDER BY i.{order_by} {order}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        pantry = cursor.fetchall()
        cursor.close()
        return pantry

    def get_filtered_recipe(self, order_by, order, name_search, ingredient_search, category_search):
        if order == "Ascending":
            order = "ASC"
        elif order == "Descending":
            order = "DESC"
        else:
            order = "ASC"
        clauses = []
        if name_search:

            clauses.append(f" WHERE recipe_name LIKE '%{name_search}%'")

        if category_search:
            clauses.append(f"category LIKE '%{category_search}% ")

        if ingredient_search:
            clauses.append(f"i.item_name LIKE '%{ingredient_search}%'")





        if order_by == "rating":
            order_by = "cookrat,avg_rating"

        query = f"""
                SELECT recipe.*, CASE WHEN cookrat.avg_rating IS NULL THEN recipe.rating ELSE cookrat.avg_rating END
                FROM recipe FULL JOIN
                    (SELECT AVG(user_rating) as avg_rating, ruid FROM cooks GROUP BY ruid)
                    as cookrat ON cookrat.ruid=recipe.ruid
                    INNER JOIN \"recipeContains\" rC on recipe.ruid = rC.ruid 
                    INNER JOIN ingredient i on i.ingredient_id = rC.ingredient_id 
                    {' AND '.join(clauses)} 
                    ORDER BY {order_by} {order}
                """

        #query = f"SELECT recipe.* FROM recipe " \
        #        f"INNER JOIN \"recipeContains\" rC on recipe.ruid = rC.ruid " \
        #        f"INNER JOIN ingredient i on i.ingredient_id = rC.ingredient_id "\
        #        f"{' AND '.join(clauses)} " \
        #        f"ORDER BY {order_by} {order} limit 50"

        cursor = self.connection.cursor()
        cursor.execute(query)
        recipe = cursor.fetchall()
        cursor.close()
        return recipe
