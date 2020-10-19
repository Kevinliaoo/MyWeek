import tkinter as tk
from Constants import Constants


class Popup(tk.Tk):

    def __init__(self, title, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(Constants.POPSIZE)
        self.resizable(False, False)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.destroyFrame)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self._buildFrame()

    def _buildFrame(self):
        """This method should be overriden in child classes"""
        pass

    def destroyFrame(self):
        """Destroy the window"""
        self.quit()
        self.destroy()