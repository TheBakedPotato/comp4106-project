

class Player:

    def __init__(self, color):
        self.color = color
        self.hashCode = hash(self.color)

    def move(self, game):
        return None


    def __eq__(self, other):
        return self.color == other.color


    def __ne__(self, other):
        return not self.color == other.color


    def __hash__(self):
        self.hashCode