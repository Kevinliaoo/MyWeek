class Time:
    HOURS = [
        ' 6 AM ~  7 AM', ' 7 AM ~  8 AM', ' 8 AM ~  9 AM', ' 9 AM ~ 10 AM',
        '10 AM ~ 11 AM', '11 AM ~ 12 PM', '12 PM ~  1 PM', ' 1 PM ~  2 PM', ' 2 PM ~  3 PM',
        ' 3 PM ~   4 PM', ' 4 PM ~  5 PM', ' 5 PM ~  6 PM', ' 6 PM ~  7 PM', ' 7 PM ~  8 PM',
        ' 9 PM ~ 10 PM', '10 PM ~ 11 PM'
    ]
    WEEKDAYS = [
        '', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]
    TIMELIST = [
        ' 6 AM', ' 7 AM', ' 8 AM', ' 9 AM', '10 AM', '11 AM', '12 PM', ' 1 PM',
        ' 2 PM', ' 3 PM', ' 4 PM', '5 PM', ' 6 PM', ' 7 PM', ' 8 PM', ' 9 PM',
        '10 PM', '11 PM'
    ]

class Constants:

    # Colors
    WHITE = (255, 255, 255)

    # Fonts
    LARGE_FONT = ("Verdana", 12)
    MEDIUM_FONT = ('Verdana', 10)
    TITLE_FONT = ('Verdana', 16)

    # MainWindow
    MAINWINDOWHEIGHT = 650
    MAINWINDOWWIDTH = 1000
    MAINWINDOWSIZE = '{}x{}'.format(MAINWINDOWWIDTH, MAINWINDOWHEIGHT)

    # Popup windows
    POPHEIGHT = 500
    POPWIDTH = 350
    POPSIZE = '{}x{}'.format(POPWIDTH, POPHEIGHT)
    TASKS = [
        "Exam", "School", "Study", "Free", "Work", "Extra curricular", "Sleep"
    ]
    SUBJECTS = [
        "Mathemathics", "Physics", "Chemestry", "English", "History"
    ]

    # JSON
    DBDIR = "./Database/database.json"
    DATA = {day: [{hour: {}} for hour in Time.HOURS] for day in Time.WEEKDAYS[1:]}
