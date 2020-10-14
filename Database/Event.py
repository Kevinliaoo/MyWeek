class Event:
    name = str
    start = str
    end = str
    day = str
    type = str
    subject = str

    def __init__(self, name, start, end, day, type, subject=None):
        self.name = name
        self.start = start
        self.end = end
        self.day = day
        self.type = type
        self.subject = subject