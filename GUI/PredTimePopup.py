import tkinter as tk
import datetime
from Constants import Time, Constants
from Database.Database import Database


class PredTimePopup(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Get current weekday
        self.today = Time.WEEKDAYS[datetime.datetime.today().weekday()+1]
        self.exams = []
        # Get all exams and store them in self.exams
        for day in Time.WEEKDAYS[1:]:

            for i in range(len(Time.HOURS)):
                data = Database.pick(day, i)

                if data != {}:
                    if data['type'] == "Exam":
                        if data not in self.exams:
                            self.exams.append(data)

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(Constants.POPSIZE)
        self.resizable(False, False)
        self.title("Target grades")
        self.protocol("WM_DELETE_WINDOW", self.destroyFrame)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        print(self.exams)

    def destroyFrame(self):
        """Destroy the window"""
        self.quit()
        self.destroy()