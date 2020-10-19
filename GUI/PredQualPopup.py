import tkinter as tk
from Constants import Time, Constants
from Database.Database import Database
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
            self.container, text = "{} ({}): {}".format(exam['name'], exam['subject'], qual),
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

        return np.round(preds[0])

    def _getStudy(self, exam):
        """
        Iterate through database and get ammount of hours of studytime

        :return: Studytime (Integer)
        """
        # Get the ammount of studytime
        studytime = 0
        # Iterate
        for day in Time.WEEKDAYS[1:]:
            for i in range(len(Time.HOURS)):
                # Pick data
                data = Database.pick(day, i)
                # Check if no null data
                if data != {}:
                    # Check if is study
                    if data['type'] == "Study":
                        # Check if subject matches with exam's subject
                        if data['subject'] == exam['subject']:
                            # Check if studytime is within today and exam date
                            iStudy = Time.WEEKDAYS.index(data['day'])
                            iExam = Time.WEEKDAYS.index(exam['day'])
                            iToday = Time.WEEKDAYS.index(self.today)

                            # If today is before exam
                            if iToday < iExam:
                                if iToday <= iStudy and iStudy < iExam:
                                    studytime += 1
                            # If today is after exam (exam will be next week)
                            if iToday > iExam:
                                if iStudy >= iToday:
                                    studytime += 1
                                if iStudy < iExam:
                                    studytime += 1
                            # Get remaining time before exam in the same day
                            if iStudy == iExam:
                                for t in Time.TIMELIST:
                                    # data reaches first
                                    if data['start'] == t:
                                        studytime += 1
                                        break
                                    # exam reaches first
                                    if exam['start'] == t:
                                        break
        return studytime
