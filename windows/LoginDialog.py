import tkinter as tk
import pyodbc
import tkinter.messagebox as mb
import controllers.DatabaseController as lc


class LoginDialog:
    """
    This class creates a login dialog window.
    """

    def __init__(self, root):
        """
        Initialize the LoginDialog with a root window.

        Parameters:
        root (tkinter.Tk): The root window for the dialog.
        """
        self.window = self._create_window(root)
        self.username_entry, self.password_entry = self._add_content()

    def _create_window(self, root):
        """
        Create a new window for the dialog.

        Parameters:
        root (tkinter.Tk): The root window for the dialog.

        Returns:
        tkinter.Toplevel: The dialog window.
        """
        window = tk.Toplevel(root)
        screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
        window_width, window_height = 300, 200
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        window.minsize(300, 200)
        return window

    def _add_content(self):
        """
        Add content to the dialog window.

        Returns:
        tuple: The username and password entry widgets.
        """
        container = tk.Frame(self.window)
        container.pack(fill="both", expand=True)

        username_label = tk.Label(container, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(container)
        username_entry.pack()

        password_label = tk.Label(container, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(container, show="*")
        password_entry.pack()

        login_button = tk.Button(container, text="Login", command=self._login)
        login_button.pack()

        return username_entry, password_entry

    def _login(self):
        """
        Log in to the application.

        This method gets the username and password from the entry widgets, tries to log in to the database, and closes the dialog window if successful.
        """
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        try:
            if lc.DatabaseController(self.username, self.password).get_tables():
                self.window.destroy()
        except pyodbc.InterfaceError:
            mb.showerror(title="Error",
                         message=f"Login failed for {self.username}. Please check username or password is correct.")

