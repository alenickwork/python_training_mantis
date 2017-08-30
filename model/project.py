from sys import maxsize

class Project:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def name_or_null(self):
        if self.name:
            return self.name
        else:
            return ""