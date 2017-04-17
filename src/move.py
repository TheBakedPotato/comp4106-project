

class Move:

    def __init__(self, player, column):
        self.player = player
        self.column = column
        self.hashCode = hash((self.player.hashCode, column))


    def __eq__(self, other):
        return (self.player == other.player) and (self.column == other.column)


    def __ne__(self, other):
        return not self == other


    def __hash__(self):
        return self.hashCode