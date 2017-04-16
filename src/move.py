

class Move:

    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos
        self.hashCode = hash((self.startPos.hashCode, self.endPos.hashCode))


    def __eq__(self, other):
        return (self.startPos == other.startPos) and (self.endPos == other.endPos)


    def __ne__(self, other):
        return not self == other


    def __hash__(self):
        return self.hashCode