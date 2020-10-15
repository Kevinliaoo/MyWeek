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
            self.container, text = self.event['name'], font = Constants.TITLE_FONT
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

    def destroyFrame(self):
        """Destroy the window"""
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
                    Database.delete(self.weekday, index)
                    break

                if started:
                    # Delete events
                    Database.delete(self.weekday, index)

                index += 1

            self.destroyFrame()

        else: return

    def _edit(self):
        """
        This function asks the user for a new name of the event and changes it (by deleting
        the old one and inserting a new Event)

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

        # Create a new Event with the new name
        newEvent = Event(
            newName, self.event['start'], self.event['end'], self.event['day'],
            self.event['type'], self.event['subject']
        )
        # Change name
        self.event['name'] = newName

        # Iterate
        started = False
        index = 0
        for t in Time.HOURS:

            # Start counting when start time is detected
            if t[0:5] == self.event['start']: started = True
            if t[8:] == self.event['end']:
                started = False
                # One last element
                Database.delete(self.weekday, index)
                Database.insert(self.weekday, index, newEvent)
                break

            if started:
                # Delete and add new Event
                Database.delete(self.weekday, index)
                Database.insert(self.weekday, index, newEvent)

            index += 1

        self._build_frame()