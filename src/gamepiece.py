

class GamePiece:

    def __init__(self, color, directions):
        self.color = color
        self.directions = directions


    def __eq__(self, other):
        return self.color == other.color


    def __ne__(self, other):
        return not (self.color == other.color)