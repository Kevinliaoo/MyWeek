import tkinter as tk
from Constants import Constants

class MainWindow(tk.Tk):
    """
    Main Window
    """

    def __init__(self, *args, **kwargs):
        # Window settings
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(Constants.MAINWINDOWSIZE)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        # GridLayout configurations
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=10)
        container.grid_columnconfigure(0, weight=1)

        # Create menu bar
        menuFrame = tk.Frame(container)
        timetableBtn = tk.Button(menuFrame, text="My time table")
        timetableBtn.grid(row=0, column=0, sticky='W', pady=10, padx=10)
        menuFrame.grid(row=0, column=0, sticky='N')

        # Frames
        self.frames = {}
        # Add frames
        for frameType in (TimeTablePage, PageOne, PageTwo):
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

class TimeTablePage(tk.Frame):
    """
    Time table Frame
    """
    HOURSROWS = len(Constants.HOURS)
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

        # Time table layout
        tableFrame = tk.Frame(self)
        # Create the timetable
        for i in range(self.HOURSROWS):

            self.l = tk.Label(tableFrame, text=Constants.HOURS[i], font=Constants.MEDIUM_FONT, padx=10)
            self.l.grid(row=i, column=0)

            for j in range(self.DAYSROWS):

                self.e = tk.Button(
                    tableFrame, width = 14, height = 1, font = Constants.MEDIUM_FONT,
                    command = lambda: print(self.e.grid_info["row"], self.e.grid_info["column"])
                )
                self.e.grid(row=i, column=j+1)

        tableFrame.grid(row=1, column=0)













class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=Constants.LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.showFrame(TimeTablePage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.showFrame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=Constants.LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.showFrame(TimeTablePage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.showFrame(PageOne))
        button2.pack()