from controllers.DatabaseController import DatabaseController


class ItemsController(DatabaseController):
    """
    This class is a controller for handling items in the database.
    It inherits from the DatabaseController class.
    """

    def __init__(self, username, password):
        """
        Initialize the ItemsController with a username and password.

        Parameters:
        username (str): The username for the database.
        password (str): The password for the database.
        """
        super().__init__(username, password)

    @staticmethod
    def create_string(columns, values):
        """
        Create a string for SQL queries.

        Parameters:
        columns (list): The columns for the query.
        values (list): The values for the query.

        Returns:
        str: A string for SQL queries.
        """
        result = []
        for column, value in zip(columns, values):
            if isinstance(value, str):
                result.append(f"{column} = '{value}'")
            else:
                result.append(f"{column} = {value}")
        return ', '.join(result)

    def create(self, table_name, columns: list, data: list):
        """
        Create a new item in the database.

        Parameters:
        table_name (str): The name of the table.
        columns (list): The columns for the new item.
        data (list): The data for the new item.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(data)});")
        self.conn.commit()

    def update(self, table_name, id, columns, data):
        """
        Update an item in the database.

        Parameters:
        table_name (str): The name of the table.
        id (int): The ID of the item.
        columns (list): The columns to update.
        data (list): The new data.
        """
        cursor = self.conn.cursor()
        update_string = ItemsController.create_string(columns, data)
        cursor.execute(
            f"UPDATE {table_name} SET {update_string} WHERE Id = {id}")
        self.conn.commit()

    def delete(self, table_name, id):
        """
        Delete an item from the database.

        Parameters:
        table_name (str): The name of the table.
        id (int): The ID of the item.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE "
                       f"Id = {id}")
        self.conn.commit()
