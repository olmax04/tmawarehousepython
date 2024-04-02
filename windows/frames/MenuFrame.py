import tkinter.messagebox as mb
import tkinter as tk
import shutil
from tkinter import filedialog

from controllers.ItemsController import ItemsController
from controllers.RequestsController import RequestsController
from windows.MainWindow import MainWindow
from windows.dialogs.OrderDialog import OrderDialog
from windows.dialogs.RequestDialog import RequestDialog
from windows.frames.TableFrame import TableFrame

class MenuFrame(tk.Menu):
    """
    This class creates a menu frame in the application.
    It inherits from the tk.Menu class.
    """

    def __init__(self, root, table_frame):
        """
        Initialize the MenuFrame with a root window and a table frame.

        Parameters:
        root (MainWindow): The root window for the menu.
        table_frame (TableFrame): The table frame for the menu.
        """
        super().__init__(root)
        self.image_entry = None
        self.root: MainWindow = root
        self.table_frame: TableFrame = table_frame
        self.root.configure(menu=self)
        self._add_content()

    def bind_to_listbox(self, listbox):
        """
        Bind the menu to a listbox widget.

        Parameters:
        listbox (tkinter.Listbox): The listbox widget to bind to.
        """
        listbox.bind("<<ListboxSelect>>", self.update_menu)

    def update_menu(self, event):
        """
        Update the menu when a listbox selection changes.

        Parameters:
        event (tkinter.Event): The event that triggered the update.
        """
        self.table_frame.switch_table()
        self.delete(0, 'end')
        self._add_content()

    def _add_content(self):
        """
        Add content to the menu.
        """
        table_name = self.get_key_by_value(self.table_frame.table)
        if table_name.lower() == "items":
            if self.root.database.has_permission(table_name, "SELECT"):
                self.add_command(label="Order", command=self.order_entry)
        if table_name.lower() == "requests":
            if self.root.database.has_permission(table_name, "SELECT") and self.root.database.has_permission("RequestsRows,", "SELECT") :
                self.add_command(label="Open Request", command=self.request_dialog)
            if self.root.database.has_permission(table_name, "UPDATE"):
                self.add_command(label="Confirm", command=self.confirm_entry)
                self.add_command(label="Reject", command=self.reject_entry)

        if self.root.database.has_permission(table_name, "INSERT"):
            self.add_command(label="Create Record", command=self.add_entry)
        else:
            self.add_command(label="Create Record", command=self.add_entry, state="disabled")

        if self.root.database.has_permission(table_name, "UPDATE"):
            self.add_command(label="Edit Record", command=self.edit_entry)
        else:
            self.add_command(label="Edit Record", command=self.edit_entry, state="disabled")
        if self.root.database.has_permission(table_name, "DELETE"):
            self.add_command(label="Delete Record", command=self.delete_entry)
        else:
            self.add_command(label="Delete Record", command=self.delete_entry, state="disabled")

    def get_key_by_value(self, value):
        """
        Get the key for a given value in the table frame's tables dictionary.

        Parameters:
        value (str): The value to find the key for.

        Returns:
        str: The key for the given value.
        """
        for key, val in self.table_frame.tables.items():
            if val == value:
                return key
        return None

    def add_entry(self):
        """
        Create a new entry in the database.

        This method creates a new dialog window, collects user input, and adds a new entry to the database.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("New Entry")

        entries = []

        table_name = self.get_key_by_value(self.table_frame.table)
        columns = self.root.database.get_columns(table_name)
        for i, field in enumerate(columns):
            if field.lower() == "id":
                continue
            label = tk.Label(dialog, text=f"Enter {field}:")
            label.grid(row=i, column=0)
            if field.lower() == "itemgroup" or field.lower() == "unit":
                selected_option = tk.StringVar(dialog)
                if field.lower() == "unit":
                    options = ["kg", "count", "boxes"]
                else:
                    options = ["color", "production", "export"]
                selected_option.set(options[0])
                dropdown = tk.OptionMenu(dialog, selected_option, *options)
                dropdown.grid(row=i, column=1)
                entries.insert(i, selected_option)
            elif field.lower() == "photo":
                file_button = tk.Button(dialog, text="Upload", command=self.upload_file)
                file_button.grid(row=i, column=1)
            else:
                entry = tk.Entry(dialog)
                entry.grid(row=i, column=1)
                entries.insert(i, entry)

        def submit():
            """
            Submit the form and create a new entry in the database.

            This method collects the user input, creates a new ItemsController, and calls its create method to add a new entry to the database.
            """
            data = [entry.get() for entry in entries]
            if self.image_entry:
                data.insert(len(data), self.image_entry)
            controller = ItemsController(self.root.database.username, self.root.database.password)
            if "Status" in columns:
                columns.remove("Status")
            controller.create(table_name, columns, data)
            self.table_frame.table.insert('', 'end', values=data)
            dialog.destroy()

        submit_button = tk.Button(dialog, text="Submit", command=submit)
        submit_button.grid(row=len(columns), column=0, columnspan=2)

    def upload_file(self):
        """
        Upload a file and save it to the assets directory.

        This method opens a file dialog, copies the selected file to the assets directory, and stores the file path in the image_entry attribute.
        """
        root = tk.Tk()
        root.withdraw()
        root.filepath = filedialog.askopenfilename(initialdir="/", title="Choose file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        shutil.copy(root.filepath, "assets")
        root.destroy()
        self.image_entry = f"assets/{root.filepath.split('/')[-1]}"

    def edit_entry(self):
        """
        Edit an existing entry in the database.

        This method creates a new dialog window, collects user input, and updates the selected entry in the database.
        """
        selected_item = self.table_frame.table.selection()
        item_values = self._get_selected_item_values()
        if item_values:
            selected_item = selected_item[0]
            item_values = self.table_frame.table.item(selected_item, "values")

            dialog = tk.Toplevel(self.root)
            dialog.title("Edit Entry")
            dialog.minsize(500, 400)
            entries = []

            table_name = self.get_key_by_value(self.table_frame.table)
            columns = self.root.database.get_columns(table_name)
            for i, field in enumerate(columns):
                if field.lower() == "id":
                    continue
                label = tk.Label(dialog, text=f"Enter {field}:")
                label.grid(row=i, column=0)
                if field.lower() == "itemgroup" or field.lower() == "unit":
                    selected_option = tk.StringVar(dialog)
                    if field.lower() == "unit":
                        options = ["kg", "count", "boxes"]
                    else:
                        options = ["color", "production", "export"]
                    dropdown = tk.OptionMenu(dialog, selected_option, *options)
                    dropdown.grid(row=i, column=1)
                    entries.insert(i, selected_option)
                    selected_option.set(item_values[i])
                elif field.lower() == "photo":
                    file_button = tk.Button(dialog, text="Upload", command=self.upload_file)
                    file_button.grid(row=i, column=1)
                else:
                    entry = tk.Entry(dialog)
                    entry.grid(row=i, column=1)
                    entry.insert(0, item_values[i])
                    entries.insert(i, entry)

            def submit():
                """
                Submit the form and update the selected entry in the database.

                This method collects the user input, creates a new ItemsController, and calls its update method to update the selected entry in the database.
                """
                data = [entry.get() for entry in entries]
                columns.pop(0)
                if self.image_entry:
                    data.insert(len(data), self.image_entry)
                controller = ItemsController(self.root.database.username, self.root.database.password)
                controller.update(table_name, item_values[0], columns, data)
                data.insert(0, item_values[0])
                self.table_frame.table.item(selected_item, values=data)
                dialog.destroy()

            submit_button = tk.Button(dialog, text="Submit", command=submit)
            submit_button.grid(row=len(columns), column=0, columnspan=2)

    def delete_entry(self):
        """
        Delete an existing entry from the database.

        This method deletes the selected entry from the database.
        """
        selected_item = self.table_frame.table.selection()
        item_values = self._get_selected_item_values()
        if item_values:
            selected_item = selected_item[0]
            item_values = self.table_frame.table.item(selected_item, "values")
            table_name = self.get_key_by_value(self.table_frame.table)
            controller = ItemsController(self.root.database.username, self.root.database.password)
            controller.delete(table_name, item_values[0])
            self.table_frame.table.delete(selected_item[0])

    def order_entry(self):
        """
        Create a new order entry.

        This method creates a new OrderDialog window and waits for it to close.
        """
        selected_item = self.table_frame.table.selection()
        if not selected_item:
            mb.showerror(title="Error", message="Not selected row")
            return
        selected_item = selected_item[0]
        item_values = self.table_frame.table.item(selected_item, "values")

        order_dialog = OrderDialog(self.root, item_values)
        self.root.wait_window(order_dialog.window)

    def request_dialog(self):
        """
        Open a request dialog.

        This method creates a new RequestDialog window and waits for it to close.
        """
        selected_item = self.table_frame.table.selection()
        if not selected_item:
            mb.showerror(title="Error", message="Not selected row")
            return
        selected_item = selected_item[0]
        item_values = self.table_frame.table.item(selected_item, "values")

        order_dialog = RequestDialog(self.root, item_values)
        self.root.wait_window(order_dialog.window)

    def confirm_entry(self):
        """
        Confirm a request.

        This method changes the status of a request to "Confirmed".
        """
        self._change_request_status("Confirmed", "Status set to confirmed on request {}")

    def reject_entry(self):
        """
        Reject a request.

        This method changes the status of a request to "Rejected".
        """
        self._change_request_status("Rejected", "Status set to rejected on request {}")

    def _get_selected_item_values(self):
        """
        Get the values of the selected item in the table.

        Returns:
        list: The values of the selected item.
        """
        selected_item = self.table_frame.table.selection()
        if not selected_item:
            mb.showerror(title="Error", message="Not selected row")
            return None
        selected_item = selected_item[0]
        return self.table_frame.table.item(selected_item, "values")

    def _change_request_status(self, status, message):
        """
        Change the status of a request.

        This method changes the status of a request and updates the table.

        Parameters:
        status (str): The new status for the request.
        message (str): The message to display when the status is changed.
        """
        selected_item = self.table_frame.table.selection()
        item_values = self._get_selected_item_values()
        if item_values:
            item_values = list(item_values)
            item_values[3] = status
            try:
                db: RequestsController = RequestsController(self.root.database.username, self.root.database.password)
                db.set_status(status, item_values[0])
                mb.showinfo("Status Change", message.format(item_values[0]))
                self.table_frame.table.item(selected_item, values=item_values)
            except Exception as e:
                mb.showerror("Status Change", f"Error on set status to {status} on request {item_values[0]}")

