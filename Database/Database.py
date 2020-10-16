import json
from tkinter import messagebox
from Constants import Constants, Time


class Database:
    """
    This class makes CRUD operations for database
    """

    @staticmethod
    def reset():
        """Resets all data of the database"""
        with open(Constants.DBDIR, "w") as write_file:
            json.dump(Constants.DATA, write_file, indent=4)

    @staticmethod
    def insert(day, timeRange, event):
        """
        Insert a new Event to database

        :param day: Day of the event
        :param timeRange: Index value of Time.HOURS
        :param event: Event to be added
        :return: None
        """
        with open(Constants.DBDIR, "r") as read_file:
            # Get data from database
            data = json.load(read_file)

        selected = data[day][timeRange][Time.HOURS[timeRange]]

        # Check if already scheduled
        if selected != {}:
            response = messagebox.askquestion(
                "Already scheduled!",
                "There is already an event scheduled at {}\nDo you want to override the event?".format(
                    Time.HOURS[timeRange]
                )
            )
            if response == "yes":
                Database.edit(day, timeRange, event)
            return

        # Add new Event Object
        selected['name'] = event.name
        selected['start'] = event.start
        selected['end'] = event.end
        selected['day'] = event.day
        selected['type'] = event.type
        selected['subject'] = event.subject
        selected['absences'] = 0
        selected['failures'] = 0

        with open(Constants.DBDIR, "w") as write_file:
            # Add new data to database
            json.dump(data, write_file, indent=4)

    @staticmethod
    def pick(day, timerange):
        """
        Select the event of a specified date and time

        :param day: String value of the day
        :param timerange: Index value of Time.HOURS
        :return: dictionary
        """
        with open(Constants.DBDIR, "r") as read_file:
            data = json.load(read_file)
            return data[day][timerange][Time.HOURS[timerange]]

    @staticmethod
    def edit(day, timeRange, newEvent):
        """
        Edits the Event in a day at a specific time

        :param day: Day of the event
        :param timeRange: Index value of Time.HOURS
        :param event: New Event
        :return: None
        """
        with open(Constants.DBDIR, "r") as read_file:
            data = json.load(read_file)

        selected = data[day][timeRange][Time.HOURS[timeRange]]

        # Check if there really is an event scheduled
        if selected != {}:
            selected['name'] = newEvent.name
            selected['start'] = newEvent.start
            selected['end'] = newEvent.end
            selected['day'] = newEvent.day
            selected['type'] = newEvent.type
            selected['subject'] = newEvent.subject
            selected['absences'] = newEvent.absences
            selected['failures'] = newEvent.failures
        else:
            messagebox.showwarning("Error!", "No event was scheduled for {}".format(Time.HOURS[timeRange]))
            return

        with open(Constants.DBDIR, "w") as write_file:
            # Add new data to database
            json.dump(data, write_file, indent=4)

    @staticmethod
    def delete(day, timerange):
        """
        Deletes the Event in a day at a specific time

        :param day: Day of the event
        :param timeRange: Index value of Time.HOURS
        :return: None
        """
        with open(Constants.DBDIR, "r") as read_file:
            data = json.load(read_file)

        data[day][timerange][Time.HOURS[timerange]] = {}

        with open(Constants.DBDIR, "w") as write_file:
            # Add new data to database
            json.dump(data, write_file, indent=4)