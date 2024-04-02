from controllers.DatabaseController import DatabaseController


class RequestsController(DatabaseController):
    """
    This class is a controller for handling requests in the database.
    It inherits from the DatabaseController class.
    """

    def __init__(self, username, password):
        """
        Initialize the RequestsController with a username and password.

        Parameters:
        username (str): The username for the database.
        password (str): The password for the database.
        """
        super().__init__(username, password)

    def create_request(self, item_id, unit, quantity, price, comment):
        """
        Create a new request in the database.

        Parameters:
        item_id (int): The ID of the item.
        unit (str): The unit of the item.
        quantity (int): The quantity of the item.
        price (float): The price of the item.
        comment (str): The comment for the request.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"EXEC CreateRequest "
            f"@EmployeeName = '{self.username}', "
            f"@Comment = '{comment}', "
            f"@Status = 'New', "
            f"@Unit = {unit}, "
            f"@ItemId = {item_id}, "
            f"@Quantity = {quantity}, "
            f"@Price = {price}, "
            f"@RowComment = '{comment}';")
        self.conn.commit()

    def add_to(self, item_id, unit, quantity, price, comment):
        """
        Add to an existing request in the database.

        Parameters:
        item_id (int): The ID of the item.
        unit (str): The unit of the item.
        quantity (int): The quantity of the item.
        price (float): The price of the item.
        comment (str): The comment for the request.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"EXEC AddRequestToExisting "
            f"@EmployeeName = '{self.username}', "
            f"@Unit = {unit}, "
            f"@ItemId = {item_id}, "
            f"@Quantity = {quantity}, "
            f"@Price = {price}, "
            f"@RowComment = '{comment}';")
        self.conn.commit()

    def set_status(self, status, request_id):
        """
        Set the status of a request in the database.

        Parameters:
        status (str): The status to set.
        request_id (int): The ID of the request.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE Requests "
            f"SET Status = '{status}' "
            f"WHERE Id = {request_id} ;")
        self.conn.commit()

