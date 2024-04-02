import tkinter as tk

from controllers.DatabaseController import DatabaseController
from windows.LoginDialog import LoginDialog
from windows.MainWindow import MainWindow
from windows.frames.MenuFrame import MenuFrame
from windows.frames.TableFrame import TableFrame


class Application:
    """
    This class represents the main application.
    """

    def __init__(self):
        """
        Initialize the Application.
        """
        pass

    def _open_login_dialog(self):
        """
        Open a login dialog and return the entered username and password.

        Returns:
        tuple: The entered username and password.
        """
        root = tk.Tk()
        root.withdraw()
        login_dialog = LoginDialog(root)
        root.wait_window(login_dialog.window)
        return login_dialog.username, login_dialog.password

    def _open_main_window(self, database):
        """
        Open the main window of the application.

        Parameters:
        database (DatabaseController): The database controller for the application.
        """
        root = MainWindow(database)
        table_frame = TableFrame(root)
        menu_frame = MenuFrame(root, table_frame)
        menu_frame.bind_to_listbox(table_frame.menu)
        root.wait_window()

    def start(self):
        """
        Start the application.

        This method opens a login dialog, gets the entered username and password, and opens the main window if the username and password are valid.
        """
        username, password = self._open_login_dialog()
        if username and password:
            database = DatabaseController(username, password)
            self._open_main_window(database)
