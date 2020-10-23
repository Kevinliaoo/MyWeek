import tkinter as tk
from tkinter import messagebox
import numpy as np
from Constants import Constants, Time
import joblib
from Database.Database import Database
from Database.Event import Event
from GUI.MLPopup import MLPopup
import warnings
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
        self.freeTime = dict()

        tk.Label(
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
            self.container, text = 'OK', font = Constants.MEDIUM_FONT, height = 2, width = 10,
            command = lambda: self._okClicked()
        )\
            .place(x = 120, y = 600)

        tk.Label(
            self.container, text = 'Study at: ', font = Constants.MEDIUM_FONT
        )\
            .place(x = 90, y = 550)

        self.v = tk.StringVar(self.container, "Morning")
        tk.Radiobutton(
            self.container, text = "Morning", variable = self.v,
            value = "Morning"
        )\
            .place(x = 180, y = 540)
        tk.Radiobutton(
            self.container, text = "Night", variable = self.v,
            value = "Night"
        )\
            .place(x = 180, y = 560)


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
        self._predictTime()
        # Subtract studytime already scheduled
        self._adjustTime()
        for i, exam in enumerate(self.exams):
            # Schedule in time table
            self._getFreeTime()
            self._schedule(i, exam)
        # Destroy Frame
        self.destroyFrame()

    def _translateGrade(self):
        """
        Get all values of all SpinBoxes and store them to self.targetGrades
        """
        for grade in self.grades:
            self.targetGrades.append(grade.get())

    def _predictTime(self):
        """Studying time prediction"""
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

    def _adjustTime(self):
        """
        Substract already scheduled study hours to predicted values
        """
        for exam in range(len(self.exams)):
            stdTime = self._getStudy(self.exams[exam])
            self.studyTime[exam] = self.studyTime[exam] - stdTime

    def _getFreeTime(self):
        """
        Get available time (free time)
        All available time is stored in a list corresponding to it's dictionary key
        Blocks of free time are stored in the same subset
        Each hour of time is stored in a tuple, containing it's time range index

        Example:
        {
            'Monday': [
                [(1, {}), (2, {}), (3, {})],
                [12, {}]
            ]

            .....

            'Sunday': [

            ]
        }
        """
        for day in Time.WEEKDAYS[1:]:
            self.freeTime[day] = []

            # Group free time that are all together in the same slice
            slice = []
            for hour in range(len(Time.HOURS)):
                data = Database.pick(day, hour)

                if hour < len(Time.HOURS)-1:
                    nextData = Database.pick(day, hour+1)
                else:
                    nextData = None

                if data == {}:
                    if nextData == {}:
                        slice.append((hour, data))
                    else:
                        if len(slice) == 0:
                            self.freeTime[day].append([(hour, data)])
                        else:
                            slice.append((hour, data))
                            self.freeTime[day].append(slice)
                            slice = []

    def _schedule(self, i, exam):
        """
        This function schedules studytime for exams

        :param i: Index value of the exam in self.exams list
        :param exam: Exam dictionary containing exam's information
        :return: None
        """
        # Skip exams that have already scheduled studytime
        stdTime = self.studyTime[i][0]
        if stdTime <= 0:
            return

        examDay = exam['day']
        examDatIndex = Time.WEEKDAYS.index(examDay) - 1
        subject = exam['subject']
        added = False

        # Schedule studytime in an entire block
        for j in range(len(Time.WEEKDAYS)-1):
            # Get previous day index
            day = Time.WEEKDAYS[examDatIndex-j]
            if day == '':   # Skip the first element of the list
                continue

            timeBlocks = self.freeTime[day]

            # Reverse freetime if user selected to study at night
            if self.v.get() == "Night":
                newTimeBlock = []
                for b in timeBlocks[::-1]:
                    newTimeBlock.append(b[::-1])
                timeBlocks = newTimeBlock

            for block in timeBlocks:
                if added == False:
                    if len(block) >= stdTime:
                        added = True
                        for u in range(int(stdTime)):
                            self._addStudyToSchedule(subject, block[u][0], day)

    def _addStudyToSchedule(self, subject, timerangeIndex, day):
        """
        Insert an event (study time) to database, given it's data

        :param subject: Subject of the event
        :param timerangeIndex: Index of Time.HOURS list
        :param day: Day of the event
        :return: None
        """
        event = Event(
            "Study {}".format(subject),
            Time.HOURS[timerangeIndex][:5],
            Time.HOURS[timerangeIndex][9:],
            day, "Study", subject
        )
        Database.insert(day, timerangeIndex, event)

