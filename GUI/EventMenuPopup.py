import tkinter as tk
from tkinter import messagebox, simpledialog
from Constants import Constants, Time
from Database.Database import Database
from Database.Event import Event


class EventMenuPopup(tk.Tk):

    def __init__(self, eventCoords, *args, **kwargs):
        self.weekday = Time.WEEKDAYS[eventCoords[0]]
        self.timeIndex = eventCoords[1] - 1
        self.event = Database.pick(self.weekday, self.timeIndex)

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(Constants.POPSIZE)
        self.resizable(False, False)
        self.title(self.event['name'])
        self.protocol("WM_DELETE_WINDOW", self.destroyFrame)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self._build_frame()

    def _build_frame(self):
        """Build the frame"""
        row = 80
        gap = 40
        spaceX = 20

        self.tittleLabel = tk.Label(
            self.container, font = Constants.TITLE_FONT, text = self.event['name']
        )\
            .place(x = spaceX, y = spaceX)

        self.eventLabel = tk.Label(
            self.container, text = "Event: {}".format(self.event['type']),
            font = Constants.MEDIUM_FONT
        )\
            .place(x = spaceX, y = row)
        row += gap

        if self.event['subject'] != None:
            self.subjectLabel = tk.Label(
                self.container, text = "Subject: {}".format(self.event['subject']),
                font = Constants.MEDIUM_FONT
            )\
                .place(x = spaceX, y = row)
            row += gap

        self.startLabel = tk.Label(
            self.container, text = "Starts at: {}".format(self.event['start']),
            font = Constants.MEDIUM_FONT
        )\
            .place(x = spaceX, y = row)
        row += gap

        self.endLabel = tk.Label(
            self.container, text = "Ends at: {}".format(self.event['end']),
            font = Constants.MEDIUM_FONT
        )\
            .place(x = spaceX, y = row)
        row += gap

        self.dayLabel = tk.Label(
            self.container, text = "Day: {}".format(self.event['day']),
            font = Constants.MEDIUM_FONT
        )\
            .place(x = spaceX, y = row)
        row += 2 * gap

        self.editBtn = tk.Button(
            self.container, text = 'Edit event', font = Constants.MEDIUM_FONT, width=10,
            command = lambda: self._edit()
        )\
            .place(x = 40, y = row)

        self.deleteBtn = tk.Button(
            self.container, text = "Delete event", font = Constants.MEDIUM_FONT,
            command = lambda: self._delete()
        )\
            .place(x = 150, y = row)
        row += 2 * gap

        # Add Spinbox to enter ammount of absences and exam failures
        if self.event['type'] == 'Exam':

            self.defaultAbs = tk.IntVar(self.container)
            self.defaultAbs.set(int(self.event['absences']))
            self.absencesLabel = tk.Label(
                self.container, text = "Absences: ", font = Constants.MEDIUM_FONT
            )\
                .place(x = spaceX, y = row)
            self.absencesSpinner = tk.Spinbox(
                self.container, from_ = 0, to = 100, state='readonly', font = Constants.MEDIUM_FONT,
                textvariable = self.defaultAbs
            )\
                .place(x = spaceX + 100, y = row)
            row += gap

            self.defaultFails = tk.IntVar(self.container)
            self.defaultFails.set(int(self.event['failures']))
            self.failuresLabel = tk.Label(
                self.container, text = "Failures: ", font = Constants.MEDIUM_FONT
            )\
                .place(x = spaceX, y = row)
            self.failuresSpinner = tk.Spinbox(
                self.container, from_ = 0, to = 3, state='readonly', font = Constants.MEDIUM_FONT,
                textvariable = self.defaultFails
            )\
                .place(x = spaceX + 100, y = row)

    def destroyFrame(self):
        """Destroy the window"""
        # Get absence and failures
        if self.event['type'] == 'Exam':
            self._change(self.event['name'], self.defaultAbs.get(), self.defaultFails.get())

        self.quit()
        self.destroy()

    def _delete(self):
        """Delete the selected Event"""
        # Get user's response
        response = messagebox.askquestion("Delete event", "Are you sure you want to delete this event?")

        if response == "yes":
            started = False
            index = 0
            for t in Time.HOURS:

                # Start counting when start time is detected
                if t[0:5] == self.event['start']: started = True
                if t[8:] == self.event['end']:
                    started = False
                    # Delete last event
                    if self.event == Database.pick(self.weekday, index):
                        Database.delete(self.weekday, index)
                    break

                if started:
                    # Delete events
                    if self.event == Database.pick(self.weekday, index):
                        Database.delete(self.weekday, index)

                index += 1

            self.destroyFrame()

        else: return

    def _edit(self):
        """
        This function asks the user for a new name of the event and changes it

        :return: None
        """
        # Get user's response
        newName = simpledialog.askstring(title="Change name", prompt="Please insert the event's new name")
        if newName != None:
            newName = newName.strip()

        # Check if name is valid
        if newName == "" or newName == None:
            if newName != None: messagebox.showwarning("Error!", "Please insert a valid name!")
            return


        self._change(newName, 0, 0)
        self.destroyFrame()

    def _change(self, newName, absences, failures):
        """
        This function changes the event on the database

        :return: None
        """
        # Create a new Event with the new name
        newEvent = Event(
            newName, self.event['start'], self.event['end'], self.event['day'],
            self.event['type'], self.event['subject'], absences, failures
        )

        # Iterate
        started = False
        index = 0
        for t in Time.HOURS:

            # Start counting when start time is detected
            if t[0:5] == self.event['start']: started = True
            if t[8:] == self.event['end']:
                started = False
                # One last element
                if self.event == Database.pick(self.weekday, index):
                    Database.edit(self.weekday, index, newEvent)
                break

            if started:
                # Delete and add new Event
                if self.event == Database.pick(self.weekday, index):
                    Database.edit(self.weekday, index, newEvent)

            index += 1

        self.event['name'] = newName
        self.event['absences'] = absences
        self.event['failures'] = failures