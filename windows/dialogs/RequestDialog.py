import tkinter as tk
from tkinter import ttk

from windows.MainWindow import MainWindow


class RequestDialog:
    """
    This class creates a dialog window for monitor requests rows connected to request in the application.
    """

    def __init__(self, root, selected_item):
        """
        Initialize the RequestDialog with a root window and a selected item.

        Parameters:
        root (MainWindow): The root window for the dialog.
        selected_item (str): The selected item for the request.
        """
        self.root: MainWindow = root
        self.window = tk.Toplevel(root)
        self.selected_item = selected_item

        self._setup_window()
        self._add_content()

    def _setup_window(self):
        """
        Set up the window size and position.
        """
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        window_width = 500
        window_height = 400
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.window.minsize(500, 400)
        self.window.title("RequestsRows")

    def _add_content(self):
        """
        Add widgets to the window.
        """
        container = tk.Frame(self.window)
        container.pack(fill="both", expand=True)

        columns = self.root.database.get_columns("RequestsRows")
        table = ttk.Treeview(container, columns=columns, show='headings')

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=len(col) * 10)

        data = self.root.database.get_requests_rows(self.selected_item[0])
        for row in data:
            table.insert('', 'end', values=tuple(row))

        table.pack(fill="both", expand=True)
