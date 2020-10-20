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