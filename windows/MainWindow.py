import tkinter as tk


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.eval('tk::PlaceWindow . center')
