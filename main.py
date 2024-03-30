# Created by olmax04
from windows.MainWindow import MainWindow
from windows.LoginDialog import LoginDialog

if __name__ == "__main__":
    root = MainWindow()
    root.withdraw()
    login = LoginDialog(root)
    root.mainloop()
