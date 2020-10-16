from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from Constants import Constants, Time, Frames
from Database.Database import Database
from Database.Event import Event

class AddEventPopup(tk.Tk):
    """
    TODAVIA TENGO UN BUG QUE RESOLVER
    RESOLVER EL PROBLEMA DE COMO OCULTAR EL COMBOBOX EXTRA
    """
    col1 = 20
    col2 = 130
    startY = 70
    yGap = 40
    row = 0
    subjectAdded = False

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(Constants.POPSIZE)
        self.resizable(False, False)
        self.title("Add event")
        self.protocol("WM_DELETE_WINDOW", self.destroyFrame)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self._buildFrame()

    def _buildFrame(self):
        """Builds the form"""

        self.tittleLabel = tk.Label(self.container, text='Add a new event', font=Constants.TITLE_FONT)
        self.tittleLabel.place(x=60, y=10)

        self.nameLabel = tk.Label(self.container, text='Event name: ', font=Constants.MEDIUM_FONT)
        self.nameEntry = tk.Entry(self.container, font=Constants.MEDIUM_FONT)
        self._placeWidgets(self.nameLabel, self.nameEntry)

        self.startLabel = tk.Label(self.container, text='Start time: ', font=Constants.MEDIUM_FONT)
        self.startCombo = ttk.Combobox(self.container)
        self.startCombo['values'] = Time.TIMELIST
        self.startCombo['state'] = "readonly"
        self._placeWidgets(self.startLabel, self.startCombo)

        self.endLabel = tk.Label(self.container, text='End time: ', font=Constants.MEDIUM_FONT)
        self.endCombo = ttk.Combobox(self.container)
        self.endCombo['values'] = Time.TIMELIST
        self.endCombo['state'] = "readonly"
        self._placeWidgets(self.endLabel, self.endCombo)

        self.dayLabel = tk.Label(self.container, text="Day: ", font=Constants.MEDIUM_FONT)
        self.dayCombo = ttk.Combobox(self.container)
        self.dayCombo['values'] = Time.WEEKDAYS[1:]
        self.dayCombo['state'] = "readonly"
        self._placeWidgets(self.dayLabel, self.dayCombo)

        self.typeLabel = tk.Label(self.container, text='Event type', font=Constants.MEDIUM_FONT)
        self.typeCombo =ttk.Combobox(self.container)
        self.typeCombo['values'] = Constants.TASKS
        self.typeCombo['state'] = "readonly"
        self.typeCombo.bind("<<ComboboxSelected>>", self._selection_changed)
        self._placeWidgets(self.typeLabel, self.typeCombo)

        self.row += 2
        self.cancelBtn = tk.Button(self.container, text='Cancel', font=Constants.MEDIUM_FONT, width=10, command=lambda: self.destroyFrame())
        self.okBtn = tk.Button(self.container, text='Ok', font=Constants.MEDIUM_FONT, width=10, command=lambda: self._btnClicked())
        self._placeWidgets(self.cancelBtn, self.okBtn)
        self.row -= 3

        self.subjectLabel = tk.Label(self.container, text='Select subject: ', font=Constants.MEDIUM_FONT)
        self.subjectCombo = ttk.Combobox(self.container)
        self.subjectCombo['values'] = Constants.SUBJECTS
        self.subjectCombo['state'] = "readonly"

    def _placeWidgets(self, label, widget):
        """
        Place two widgets one next to the other and makes a breakline
        """
        label.place(x=self.col1, y=self.startY+self.row*self.yGap)
        widget.place(x=self.col2, y=self.startY+self.row*self.yGap)
        self.row += 1

    def _selection_changed(self, event):
        """
        Show subject Combobox
        THERE IS A BUG TO FIX
        """
        if self.typeCombo.get() in Constants.TASKS[0:3]:
            if self.subjectAdded == False:
                self._placeWidgets(self.subjectLabel, self.subjectCombo)
                self.subjectAdded = True
        else:
            if self.subjectAdded:
                # Hide subject label and combobox
                self.subjectLabel.place_forget()
                self.subjectCombo.place_forget()
                self.subjectAdded = False
                self.row -= 1

    def destroyFrame(self):
        """Destroy the window"""
        self.quit()
        self.destroy()

    def _btnClicked(self):
        """Insert data in database when OK button is clicked"""
        # Check if all fields were filled
        name = self.nameEntry.get().strip()
        start = self.startCombo.get()
        end = self.endCombo.get()
        day = self.dayCombo.get()
        type = self.typeCombo.get()

        # Check missing values
        if name == "" or start == "" or end == "" or day == "" or type == "":
            messagebox.showwarning("Missing fields!", "Please fill the missing fields!")
            return
        if type in Constants.TASKS[0:3]:
            subject = self.subjectCombo.get()
            if subject == "":
                messagebox.showwarning("Missing fields!", "Please fill the missing fields!")
                return
        else:
            subject = None

        # Check if starts earlier than end
        if Time.TIMELIST.index(start) >= Time.TIMELIST.index(end):
            messagebox.showwarning("Time error", "Make sure that time is correct!")
            return

        # Check time
        started = False
        index = 0
        for t in Time.HOURS:
            # Create an event for each hour
            if t[0:5] == start: started = True
            if t[8:] == end:
                started = False
                # Add one last event
                if subject == "":
                    event = Event(name, start, end, day, type)
                else:
                    event = Event(name, start, end, day, type, subject)
                Database.insert(day, index, event)

            if started:
                # Create the Event object
                if subject == "":
                    event = Event(name, start, end, day, type)
                else:
                    event = Event(name, start, end, day, type, subject)
                Database.insert(day, index, event)

            index += 1

        self.destroyFrame()
