import tkinter as tk

from controllers.DatabaseController import DatabaseController


class MainWindow(tk.Tk):
    """
    This class creates the main window of the application.
    It inherits from the tk.Tk class.
    """

    def __init__(self, database: DatabaseController):
        """
        Initialize the MainWindow with a database controller.

        Parameters:
        database (DatabaseController): The database controller for the application.
        """
        super().__init__()
        self.title("TMAWarehouse")
        self.eval('tk::PlaceWindow . center')
        self.state("zoomed")
        self.database = database
