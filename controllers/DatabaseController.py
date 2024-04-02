import pyodbc


class DatabaseController:
    """
    This class is a controller for handling database operations.
    """

    def __init__(self, username, password):
        """
        Initialize the DatabaseController with a username and password.

        Parameters:
        username (str): The username for the database.
        password (str): The password for the database.
        """
        self.username = username
        self.password = password
        self.conn: pyodbc.Connection or None = None
        self._connect()

    def _connect(self):
        """
        Connect to the database using the provided username and password.
        """
        self.conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "SERVER=LAPTOP-9SLKI14C\\NAVDEMO;"
                                   "DATABASE=tmawarehouse;"
                                   f"UID={self.username};"
                                   f"PWD={self.password};"
                                   "TrustedConnection=no;")

    def get_columns(self, table_name):
        """
        Get the columns of a table in the database.

        Parameters:
        table_name (str): The name of the table.

        Returns:
        list: A list of column names.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table_name}'")
        result = cursor.fetchall()
        columns = [c[0] for c in result]
        return columns

    def get_rows(self, table_name):
        """
        Get the rows of a table in the database.

        Parameters:
        table_name (str): The name of the table.

        Returns:
        list: A list of rows.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        result = cursor.fetchall()
        return result

    def get_tables(self):
        """
        Get the tables in the database.

        Returns:
        list: A list of table names.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT name FROM SYSOBJECTS WHERE xtype='u';")
        result = cursor.fetchall()
        tables = [c[0] for c in result]
        return tables

    def has_permission(self, table_name, operation):
        """
        Check if the user has permission to perform an operation on a table.

        Parameters:
        table_name (str): The name of the table.
        operation (str): The operation to check.

        Returns:
        bool: True if the user has permission, False otherwise.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT HAS_PERMS_BY_NAME('{table_name}', 'OBJECT', '{operation}');")
        result = cursor.fetchone()
        return result[0] == 1

    def get_requests_rows(self, request_id):
        """
        Get the rows of a request in the database.

        Parameters:
        request_id (int): The ID of the request.

        Returns:
        list: A list of rows.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT rr.* "
            f"FROM Requests r "
            f"JOIN RequestsRowsConnect rrc "
            f"ON r.Id = rrc.RequestId "
            f"JOIN RequestsRows rr "
            f"ON rrc.RequestsRowId = rr.Id "
            f"WHERE r.Id = {request_id};")
        result = cursor.fetchall()
        return result
