

class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hashCode = hash((x,y))

    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)


    def __ne__(self, other):
        return not (self == other)


    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)


    def __le__(self, other):
        return (self < other) or (self == other)


    def __ge__(self, other):
        return (self > other) or (self == other)


    def __hash__(self):
        return self.hashCode