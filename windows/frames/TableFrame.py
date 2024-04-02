import tkinter as tk
from tkinter import ttk


class TableFrame(tk.Frame):
    """
    This class creates a frame that contains a table.
    It inherits from the tk.Frame class.
    """

    def __init__(self, root):
        """
        Initialize the TableFrame with a root window.

        Parameters:
        root (tkinter.Tk): The root window for the frame.
        """
        super().__init__(root)
        self.root = root
        self.table = None
        self.tables = {}
        self.lc = self.root.database
        self._add_content()

    def switch_table(self, event=None):
        """
        Switch the displayed table based on the current selection in the menu.

        Parameters:
        event (tkinter.Event): The event that triggered the switch.
        """
        current_selection = self.menu.curselection()
        if current_selection:
            table_name = self.menu.get(current_selection)
            for child in self.container.winfo_children():
                child.pack_forget()
            self.table = self.tables[table_name]
            self.tables[table_name].pack(fill='both', expand=True)
            self.root.update()

    def _add_content(self):
        """
        Add content to the frame.
        """
        menu = tk.Listbox(self.root)
        self.menu = menu
        menu.pack(side="left", fill="y")

        container = ttk.Frame(self.root)
        self.container = container
        container.pack(side="right", fill='both', expand=True)
        self.photos = {}
        for table_name in self.lc.get_tables():
            columns: list = self.lc.get_columns(table_name)
            table = ttk.Treeview(container, columns=columns, show='headings')
            for col in columns:
                table.heading(col, text=col, command=lambda _col=col: self._sort_column(_col, False))
                table.column(col, width=len(col) * 10)

            for row in self.lc.get_rows(table_name):
                table.insert('', 'end', values=tuple(row))
            self.tables[table_name] = table

        menu.bind("<<ListboxSelect>>", self.switch_table)

        for table_name in self.tables.keys():
            menu.insert('end', table_name)

        menu.selection_set(0)
        self.switch_table()

    def _sort_column(self, column, reverse):
        """
        Sort the table by a column.

        Parameters:
        column (str): The column to sort by.
        reverse (bool): Whether to sort in reverse order.
        """
        data = [(self.table.set(child, column), child) for child in self.table.get_children('')]
        data.sort(reverse=reverse)

        for index, item in enumerate(data):
            self.table.move(item[1], '', index)

        self.table.heading(column, command=lambda: self._sort_column(column, not reverse))

