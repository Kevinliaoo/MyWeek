import tkinter as tk
from tkinter import messagebox

from Constants import Constants, Time
from GUI.AddEventPopup import AddEventPopup
from Database.Database import Database


class MainWindow(tk.Tk):
    """
    Main Window
    """

    def __init__(self, *args, **kwargs):
        # Window settings
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("My weekly organizer")
        self.geometry(Constants.MAINWINDOWSIZE)
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        # GridLayout configurations
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=10)
        container.grid_columnconfigure(0, weight=1)

        # Create menu bar
        menuFrame = tk.Frame(container)
        addEventBtn = tk.Button(menuFrame, text="Add event", command=lambda: self._addEvent())
        addEventBtn.grid(row=0, column=0, sticky='W', pady=10, padx=10)
        delEventBtn = tk.Button(menuFrame, text="Delete event", command=lambda: self._removeEvent())
        delEventBtn.grid(row=0, column=1, sticky='W', pady=10, padx=10)
        menuFrame.grid(row=0, column=0, sticky='N')
        predTime = tk.Button(menuFrame, text='Predict timetable')
        predTime.grid(row=0, column=2, sticky='W', padx=10, pady=10)
        predQual = tk.Button(menuFrame, text='Predict qualification')
        predQual.grid(row=0, column=3, sticky='W', padx=10, pady=10)
        clearDB = tk.Button(menuFrame, text='Clear my schedule', command=lambda: self._clearSch())
        clearDB.grid(row=0, column=4, sticky='W', padx=10, pady=10)

        # Frames
        self.frames = {}
        # Add frames
        for frameType in (TimeTablePage, ):
            frame = frameType(container, self)
            self.frames[frameType] = frame
            frame.grid(row=1, column=0, sticky="nsew")

        self.showFrame(TimeTablePage)

    def showFrame (self, cont):
        """
        Switch frames

        :param cont: Frame to change
        :return: None
        """
        frame = self.frames[cont]
        frame.tkraise()

    def _addEvent(self):
        """Show the AddEventPopup window for adding events"""
        addPop = AddEventPopup()
        addPop.mainloop()
        # Reprint table

    def _removeEvent(self):
        """Remove a single event in the timetable"""
        print("Remove event")
        Database.insert()
        Database.read()
        # Reprint table

    def _clearSch(self):
        """Clears all events of the time table"""
        response = messagebox.askquestion("Clear time table", "Are you sure you want to clear the time table?")
        if response == "yes":
            Database.reset()

class TimeTablePage(tk.Frame):
    """
    Time table Frame
    """
    HOURSROWS = len(Time.HOURS)
    DAYSROWS = 7

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # GridLayout configurations
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        # Title Layout
        titleFrame = tk.Frame(self)
        tk.Label(titleFrame, text='My time table', font=Constants.TITLE_FONT).grid(row=0, column=0)
        titleFrame.grid(row=0, column=0)

        self._buildTimeTable()

    def _buildTimeTable(self):
        """Build time table"""
        # Time table layout
        tableFrame = tk.Frame(self)
        # Create the timetable
        for k in range(len(Time.WEEKDAYS)):
            tk.Label(tableFrame, text=Time.WEEKDAYS[k], font=Constants.MEDIUM_FONT, padx=10, pady=20).grid(row=0, column=k)

        for i in range(self.HOURSROWS):
            self.l = tk.Label(tableFrame, text=Time.HOURS[i], font=Constants.MEDIUM_FONT, padx=30)
            self.l.grid(row=i+1, column=0)

            for j in range(self.DAYSROWS):

                # Get data from database
                if j > 0:
                    data = Database.pick(Time.WEEKDAYS[j], i)
                    # Check datamessagebox

                self.e = tk.Label(
                    tableFrame, width = 14, height = 1, font = Constants.MEDIUM_FONT
                )
                self.e.grid(row=i+1, column=j+2)

        tableFrame.grid(row=1, column=0)
