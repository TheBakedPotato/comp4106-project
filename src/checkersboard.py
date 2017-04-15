

class CheckersBoard:
    
    def __init__(self, size):
        self.board = {}
        self.size = size
        self.createBoard()


    def createBoard(self):
        numPieces = ((self.size / 2) - 1) * (self.size / 2)
        currCount = 0
        for y in range(self.size):
            for x in range(self.size):
                if ((x - y) % 2 == 1):
                    tilePos = (x,y)
                    self.board[tilePos] = "B"
                    currCount += 1

            if currCount == numPieces:
                break