from Constants import Time, Constants
from Database.Database import Database
import datetime
from GUI.Popups import Popup


class MLPopup(Popup):

    def __init__(self, title, *args, **kwargs):
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

        Popup.__init__(self, title, *args, **kwargs)
        self.geometry(Constants.MLPOPSIZE)

    def _buildFrame(self):
        """This method should be overriden in child classes"""
        pass

    def _getStudy(self, exam):
        """
        Iterate through database and get ammount of hours of studytime

        :param exam: Exam information
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
