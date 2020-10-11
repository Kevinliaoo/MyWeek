from tkinter import ttk
import tkinter as tk
from Constants import Constants, Time


class AddEventPopup(tk.Tk):
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
        self.protocol("WM_DELETE_WINDOW", self._destroy)

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
        self. startCombo['values'] = Time.TIMELIST
        self._placeWidgets(self.startLabel, self.startCombo)

        self.endLabel = tk.Label(self.container, text='End time: ', font=Constants.MEDIUM_FONT)
        self.endCombo = ttk.Combobox(self.container)
        self.endCombo['values'] = Time.TIMELIST
        self._placeWidgets(self.endLabel, self.endCombo)

        self.dayLabel = tk.Label(self.container, text="Day: ", font=Constants.MEDIUM_FONT)
        self.dayCombo = ttk.Combobox(self.container)
        self.dayCombo['values'] = Time.WEEKDAYS
        self._placeWidgets(self.dayLabel, self.dayCombo)

        self.typeLabel = tk.Label(self.container, text='Event type', font=Constants.MEDIUM_FONT)
        self.typeCombo =ttk.Combobox(self.container)
        self.typeCombo['values'] = Constants.TASKS
        self.typeCombo.bind("<<ComboboxSelected>>", self._selection_changed)
        self._placeWidgets(self.typeLabel, self.typeCombo)

        self.row += 2
        self.cancelBtn = tk.Button(self.container, text='Cancel', font=Constants.MEDIUM_FONT, width=10, command=lambda: self._destroy())
        self.okBtn = tk.Button(self.container, text='Ok', font=Constants.MEDIUM_FONT, width=10, command=lambda: self._btnClicked())
        self._placeWidgets(self.cancelBtn, self.okBtn)
        self.row -= 3

        self.subjectLabel = tk.Label(self.container, text='Select subject: ', font=Constants.MEDIUM_FONT)
        self.subjectCombo = ttk.Combobox(self.container)

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
        if self.typeCombo.get() == Constants.TASKS[0] or self.typeCombo.get() == Constants.TASKS[1] or self.typeCombo.get() == Constants.TASKS[2]:
            if self.subjectAdded == False:
                self._placeWidgets(self.subjectLabel, self.subjectCombo)
                self.subjectAdded = True
        else:
            if self.subjectAdded:
                # Remove
                self.subjectLabel.destroy()
                self.subjectCombo.destroy()
                self.subjectAdded = False

    def _destroy(self):
        """Destroy the window"""
        self.quit()
        self.destroy()

    def _btnClicked(self):
        print("DFEDVEFDV")
        self.subjectLabel.destroy()
        self.subjectCombo.destroy()
        # Check if all fields were filled
        # Check if starts earlier than end