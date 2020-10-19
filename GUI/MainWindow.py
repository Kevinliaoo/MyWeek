import tkinter as tk
from tkinter import messagebox
from Constants import Constants, Time, Frames
from GUI.AddEventPopup import AddEventPopup
from Database.Database import Database
from GUI.EventMenuPopup import EventMenuPopup
from GUI.PredQualPopup import PredQualPopup
from GUI.PredTimePopup import PredTimePopup


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
        self.protocol("WM_DELETE_WINDOW", self.destroyFrame)

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
        menuFrame.grid(row=0, column=0, sticky='N')
        predTime = tk.Button(menuFrame, text='Predict timetable', command=lambda: self._predictTimeTable())
        predTime.grid(row=0, column=2, sticky='W', padx=10, pady=10)
        predQual = tk.Button(menuFrame, text='Predict qualification', command=lambda: self._predQual())
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
        Frames.frames.append(addPop)
        addPop.mainloop()
        # Rebuild TimeTablePage
        try:
            self.frames[TimeTablePage].buildTimeTable()
        except:
            pass

    def _clearSch(self):
        """Clears all events of the time table"""
        response = messagebox.askquestion("Clear time table", "Are you sure you want to clear the time table?")
        if response == "yes":
            Database.reset()
            self.frames[TimeTablePage].buildTimeTable()

    def _predQual(self):
        """
        Show the PredQualPopup for predicting exam qualifications
        """
        predQual = PredQualPopup()
        Frames.frames.append(predQual)
        predQual.mainloop()

    def _predictTimeTable(self):
        """
        Predicts the ammount of studytime and free time the student can have,
        based on student's exams target grade
        """
        predTime = PredTimePopup()
        Frames.frames.append(predTime)
        predTime.mainloop()

    def destroyFrame(self):
        """Destroy the window"""
        for f in Frames.frames:
            try:
                f.destroyFrame()
            except:
                pass

        self.quit()
        self.destroy()

class TimeTablePage(tk.Frame):
    """
    Time table Frame
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        # GridLayout configurations
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        # Title Layout
        titleFrame = tk.Frame(self)
        tk.Label(titleFrame, text='My time table', font=Constants.TITLE_FONT).grid(row=0, column=0)
        titleFrame.grid(row=0, column=0)

        self.buildTimeTable()

    def buildTimeTable(self):
        """Build time table"""
        # Time table layout
        self.tableFrame = tk.Frame(self)
        # Create the timetable
        for d in range(len(Time.WEEKDAYS)):
            tk.Label(
                self.tableFrame, text = Time.WEEKDAYS[d], font = Constants.MEDIUM_FONT, padx = 25, pady = 30
            ).grid(row=0, column=d)

            if d == 0:
                for h in range(len(Time.HOURS)):
                    tk.Label(
                        self.tableFrame, text = Time.HOURS[h], font = Constants.MEDIUM_FONT, padx = 20, pady = 5
                    ).grid(row= h + 1, column = d)
            else:
                for e in range(len(Time.HOURS)):
                    data = Database.pick(Time.WEEKDAYS[d], e)
                    self.e = tk.Label(
                        self.tableFrame, width=14, height=1, font=Constants.MEDIUM_FONT
                    )

                    if data != {}:
                        self.e['text'] = data['name']
                        self.e.bind("<Button-1>", lambda ev: self._eventClicked(ev))

                    self.e.grid(row = e+1, column = d)

        self.tableFrame.grid(row=1, column=0)

    def _eventClicked(self, event):
        """
        Function triggered when a label in the timetable is clicked

        :param event: Click event
        :return: None
        """
        # Retrieve the size of the parent widget relative to master widget
        x = event.x_root - self.tableFrame.winfo_rootx()
        y = event.y_root - self.tableFrame.winfo_rooty()

        # Retreive the relative position on the parent widget
        z = self.tableFrame.grid_location(x, y) # Coordenates

        # Show event menu
        eventMenuPopup = EventMenuPopup(z)
        Frames.frames.append(eventMenuPopup)
        eventMenuPopup.mainloop()
        # Rebuild frame if was not destroyed
        try:
            self.buildTimeTable()
        except:
            pass