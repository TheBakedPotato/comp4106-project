from position import Position

class CheckersBoard:
    
    def __init__(self, size):
        self.board = {}
        self.size = size
        self.createBoard()


    def createBoard(self):
        blackYLimit = (self.size / 2) - 1
        whiteYLimit = (self.size / 2) + 1
        currCount = 0
        for y in range(self.size):
            for x in range(self.size):
                if ((x - y) % 2 == 1):
                    pos = Position(x,y)
                    if y < blackYLimit:
                        self.board[pos] = "B"
                    elif y >= whiteYLimit:
                        self.board[pos] = "W"
