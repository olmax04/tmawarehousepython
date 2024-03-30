import tkinter as tk


class LoginDialog(tk.Toplevel):

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self._settings()
        self._add_content()

    def _settings(self):
        self.minsize(300, 200)

    def _add_content(self):
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        username_label = tk.Label(container, text="Username:")
        username_label.pack()
        self.username_entry = tk.Entry(container)
        self.username_entry.pack()
        password_label = tk.Label(container, text="Password:")
        password_label.pack()
        self.password_entry = tk.Entry(container, show="*")
        self.password_entry.pack()

        login_button = tk.Button(container, text="Login", command=self._login)
        login_button.pack()

    def _login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Username: {username}, Password: {password}")
        self.destroy()
        self.root.deiconify()
