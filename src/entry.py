

class Entry:

    def __init__(self, item, value):
        self.item = item
        self.value = value


    def __eq__(self, other):
        return self.value == other.value


    def __ne__(self, other):
        return not (self == other)


    def __lt__(self, other):
        return self.value < other.value


    def __gt__(self, other):
        return self.value > other.value


    def __le__(self, other):
        return (self < other) or (self == other)


    def __ge__(self, other):
        return (self > other) or (self == other)