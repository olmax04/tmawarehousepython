import tkinter as tk
import tkinter.messagebox as mb

from controllers.RequestsController import RequestsController
from windows.MainWindow import MainWindow


class OrderDialog:
    """
    This class creates a dialog window for handling orders in the application.
    It inherits from the MainWindow class.
    """

    def __init__(self, root, selected_item):
        """
        Initialize the OrderDialog with a root window and a selected item.

        Parameters:
        root (MainWindow): The root window for the dialog.
        selected_item (str): The selected item for the order.
        """
        self.root: MainWindow = root
        self.window = tk.Toplevel(root)
        self.selected_item = selected_item
        self.request_controller = RequestsController(self.root.database.username, self.root.database.password)
        self.entires = []
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
        self.window.title("New Order")

    def _add_content(self):
        """
        Add widgets to the window.
        """
        container = tk.Frame(self.window)
        container.pack(fill="both", expand=True)

        self._add_label_and_dropdown(container, "Unit:", ["kg", "count", "boxes"])
        self._add_label_and_entry(container, "Quantity:", initial_value=self.selected_item[3])
        self._add_label_and_entry(container, "Price:")
        self._add_label_and_entry(container, "Comment:")

        self._add_button(container, "Submit", self._submit)
        self._add_button(container, "Cancel", self.window.destroy)
        self._add_button(container, "Add to request", self._add_to_request)

    def _add_label_and_entry(self, parent, label_text, initial_value=""):
        """
        Add a label and an entry widget.

        Parameters:
        parent (tkinter.Tk): The parent widget.
        label_text (str): The text for the label.
        initial_value (str): The initial value for the entry widget.

        Returns:
        tkinter.Entry: The entry widget.
        """
        tk.Label(parent, text=label_text).pack()
        entry = tk.Entry(parent)
        entry.insert(0, initial_value)
        entry.pack()
        self.entires.append(entry)
        return entry

    def _add_label(self, parent, label_text):
        """
        Add a label widget.

        Parameters:
        parent (tkinter.Tk): The parent widget.
        label_text (str): The text for the label.
        """
        tk.Label(parent, text=label_text).pack()

    def _add_label_and_dropdown(self, parent, label_text, options):
        """
        Add a label and a dropdown widget.

        Parameters:
        parent (tkinter.Tk): The parent widget.
        label_text (str): The text for the label.
        options (list): The options for the dropdown widget.

        Returns:
        tkinter.StringVar: The variable associated with the dropdown widget.
        """
        tk.Label(parent, text=label_text).pack()
        var = tk.StringVar(parent)
        var.set(options[0])
        dropdown = tk.OptionMenu(parent, var, *options)
        dropdown.pack()
        self.entires.append(var)
        return var

    def _add_button(self, parent, label_text, command):
        """
        Add a button widget.

        Parameters:
        parent (tkinter.Tk): The parent widget.
        label_text (str): The text for the button.
        command (function): The function to call when the button is clicked.
        """
        tk.Button(parent, text=label_text, command=command).pack()

    def _submit(self):
        """
        Submit the form.
        """
        self._create_or_update_request("Request created")

    def _add_to_request(self):
        """
        Add the form data to an existing request.
        """
        self._create_or_update_request("Request updated")

    def _create_or_update_request(self, success_message):
        """
        Create or update a request.

        Parameters:
        success_message (str): The message to display when the request is successful.
        """
        item_id = self.selected_item[0]
        print(item_id)
        data = [entry.get() for entry in self.entires]
        print(data)
        if success_message == "Request created":
            self.request_controller.create_request(item_id, *data)
        else:
            self.request_controller.add_to(item_id, *data)
        mb.showinfo(title="Request", message=success_message)
        self.window.destroy()
