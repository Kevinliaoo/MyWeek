import tkinter as tk
from tkinter import messagebox
import numpy as np
from Constants import Constants
import joblib
import warnings
from GUI.MLPopup import MLPopup
warnings.filterwarnings('ignore')

class PredTimePopup(MLPopup):

    def __init__(self, *args, **kwargs):
        title = "Target grades"
        MLPopup.__init__(self, title, *args, **kwargs)

    def _buildFrame(self):
        """Build the frame"""
        self.spaceX = 20
        self.spaceY = 80
        self.row = 0
        self.gap1 = 25
        self.gap2 = 60
        # Spinners
        self.spinners = []
        self.grades = []
        # User introduced grades
        self.targetGrades = []
        # Studytime predicted by Machine Learning Model
        self.studyTime = []

        titleLabel = tk.Label(
            self.container, text = "Insert your target score", font = Constants.TITLE_FONT
        )\
            .place(x = self.spaceX, y = self.spaceX)

        for exam in self.exams:
            grade = tk.IntVar(self.container)
            grade.set(6)

            self.spinners.append(tk.Spinbox(
                self.container, from_ = 1, to = 10, state = 'readonly', font = Constants.MEDIUM_FONT,
                textvariable = grade
            ))
            self.grades.append(grade)

            self._buildExam(exam)
            self.row += 1

        self.okBtn = tk.Button(
            self.container, text = 'OK', font = Constants.MEDIUM_FONT,
            command = lambda: self._okClicked()
        )\
            .place(x = 150, y = 580)

    def _buildExam(self, exam):
        """Places a label with it's SpinBox"""
        tk.Label(
            self.container, text = "{} ({}): ".format(exam['name'], exam['subject']),
            font = Constants.MEDIUM_FONT
        )\
            .place(x = self.spaceX, y = self.spaceY + self.row * self.gap2)

        self.spinners[self.row].place(x = self.spaceX, y = self.spaceY + self.row * self.gap2 + self.gap1)

    def _okClicked(self):

        # Get all user introduced grades
        self._translateGrade()
        # Predict grades
        self._predictGrades()
        # Schedule in time table
        print(self.studyTime)
        # Destroy Frame
        self.destroyFrame()

    def _translateGrade(self):
        """
        Get all values of all SpinBoxes and store them to self.targetGrades
        """
        for grade in self.grades:
            self.targetGrades.append(grade.get())

    def _predictGrades(self):
        """Grade prediction"""
        # Check for errors
        if len(self.exams) != len(self.targetGrades):
            messagebox.showwarning("Error!", "Sorry, something went wrong!")
            self.destroyFrame()
            return

        # Iterate through all exams
        for exam in range(len(self.exams)):

            # Build dataset
            failures = self.exams[exam]['failures']
            absences = self.exams[exam]['absences']
            grade = self.targetGrades[exam]
            df = np.array([[failures, absences, grade]])

            # Load Models
            mathModel = joblib.load(Constants.MATHTIMEPATH)
            portModel = joblib.load(Constants.PORTTIMEPATH)

            # Select a model
            if self.exams[exam]['subject'] in Constants.MAT_SUBJS: model = mathModel
            elif self.exams[exam]['subject'] in Constants.POR_SUBJS: model = portModel

            # Make predictions
            preds = model.predict(df)
            self.studyTime.append(np.round(preds))