import tkinter as tk
from Constants import Time, Constants
import numpy as np
import joblib
import warnings
from GUI.MLPopup import MLPopup
warnings.filterwarnings('ignore')

class PredQualPopup(MLPopup):

    def __init__(self, *args, **kwargs):
        title = "Exam qualification predictor"
        MLPopup.__init__(self, title, *args, **kwargs)

    def _buildFrame(self):
        """Build the frame"""
        self.spaceY = 80
        self.row = 0
        self.gap = 25
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
            self.container, text = "{} ({}):\t{:.2f}".format(exam['name'], exam['subject'], qual),
            font = Constants.MEDIUM_FONT
        )\
            .place(x = self.spaceX, y = self.spaceY + self.row * self.gap)

    def _predictQual(self, exam):
        """
        Gets the qualification of an exam got from the Machine Learning models

        :return: Predicted grade for the exam
        """
        # Load Machine Learning Models
        mathModel = joblib.load(Constants.MATHGRADEPATH)
        portModel = joblib.load(Constants.PORTGRADEPATH)

        # Get input dataset
        stdTime = self._getStudy(exam)
        absences = exam['absences']
        failures = exam['failures']
        df = np.array([[stdTime, failures, absences]])

        # Select a model
        if exam['subject'] in Constants.MAT_SUBJS: model = mathModel
        elif exam['subject'] in Constants.POR_SUBJS: model = portModel

        # Make predictions
        preds = model.predict(df)

        return preds[0]