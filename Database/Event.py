class Event:
    name = str
    start = str
    end = str
    day = str
    type = str
    subject = str
    absences = int
    failures = int

    def __init__(self, name, start, end, day, type, subject=None, absences=0, failures=0):
        self.name = name
        self.start = start
        self.end = end
        self.day = day
        self.type = type
        self.subject = subject
        self.absences = absences
        self.failures = failures