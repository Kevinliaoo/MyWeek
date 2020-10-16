import tkinter as tk
from tkinter import messagebox

from Constants import Time, Constants
from Database.Database import Database


class PredQualPopup(tk.Tk):

    def __init__(self, *args, **kwargs):
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
        self.title("Exam qualification predictor")
        self.protocol("WM_DELETE_WINDOW", self.destroyFrame)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self._buildFrame()

    def _buildFrame(self):
        """Build the frame"""
        self.spaceY = 80
        self.row = 0
        self.gap = 40
        self.spaceX = 20

        self.titleLabel = tk.Label(
            self.container, text = "Exams qualification predictor", font = Constants.TITLE_FONT,
        )\
            .place(x = self.spaceX, y = self.spaceX)

        for exam in self.exams:
            self._buildExam(exam)
            self.row += 1

    def _buildExam(self, exam):
        """
        Place a Label containing exam infromation on the next row

        :param exam: Exam
        :return: None
        """
        qual = self._predictQual(exam)

        tk.Label(
            self.container, text = "{}: {}".format(exam['name'], qual, font = Constants.MEDIUM_FONT)
        )\
            .place(x = self.spaceX, y = self.spaceY + self.row * self.gap)

    def _predictQual(self, exam):
        """
        Gets the qualification of an exam

        :return: Qualification note
        """
        # Get the ammount of studytime
        studytime = 0
        for day in Time.WEEKDAYS[1:]:
            for i in range(len(Time.HOURS)):
                data = Database.pick(day, i)
                if data != {}:
                    if data['type'] == "Study":
                        if data['subject'] == exam['subject']:
                            studytime += 1

        return studytime

    def destroyFrame(self):
        """Destroy the window"""
        self.quit()
        self.destroy()