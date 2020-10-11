import json
from Constants import Constants

class Database:

    @staticmethod
    def reset():
        """Resets all data from database"""
        with open(Constants.DBDIR, "w") as write_file:
            json.dump(Constants.DATA, write_file, indent=4)

    @staticmethod
    def insert():
        """Insert data to database"""
        with open(Constants.DBDIR, "w") as write_file:
            json.dump(Constants.DATA, write_file, indent=4)

    @staticmethod
    def read():
        """Read database"""
        with open(Constants.DBDIR, "r") as read_file:
            data = json.load(read_file)
            print(data)