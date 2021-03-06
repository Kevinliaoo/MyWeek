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
        ' 2 PM', ' 3 PM', ' 4 PM', ' 5 PM', ' 6 PM', ' 7 PM', ' 8 PM', ' 9 PM',
        '10 PM', '11 PM'
    ]

class Frames:
    frames = []

class Constants:

    # Colors
    WHITE = (255, 255, 255)

    # Colors for Time table
    GRIDCOLOR = [
        ('#ff8f8f', '#4a0000'), # Red
        ('#ffd382', '#5e3d00'), # Orange
        ('#d5ff87', '#3f6100'), # Lime
        ('#94ff9f', '#005409'), # Green
        ('#87ffd9', '#006b49'), # turqoise
        ('#8a92ff', '#000c5c'), # Blue
        ('#d796ff', '#39005c')  # Purple
    ]
    TODAY = ('#000000', '#ffffff')

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
    MLPOPSIZE = "350x650"
    TASKS = [
        "Exam", "School", "Study", "Free", "Work", "Extra curricular", "Sleep"
    ]
    MAT_SUBJS = [
        "Mathemathics", "Physics", "Chemestry"
    ]
    POR_SUBJS = [
        "English", "History"
    ]
    SUBJECTS = MAT_SUBJS + POR_SUBJS

    # JSON
    DBDIR = "./Database/database.json"
    DATA = {day: [{hour: {}} for hour in Time.HOURS] for day in Time.WEEKDAYS[1:]}

    # Machine Learning
    MATHGRADEPATH = "./Machine_learning/Models/mat_grade_pred.pkl"
    PORTGRADEPATH = "./Machine_learning/Models/por_grade_pred.pkl"
    MATHTIMEPATH = "./Machine_learning/Models/mat_time_pred.pkl"
    PORTTIMEPATH = "./Machine_learning/Models/por_time_pred.pkl"