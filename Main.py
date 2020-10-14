from Database.Database import Database
from GUI.MainWindow import MainWindow

if __name__ == '__main__':

    Database.reset()
    app = MainWindow()
    app.mainloop()