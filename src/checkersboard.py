from position import Position
from gamepiece import GamePiece

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
                        self.board[pos] = GamePiece("B", [1])
                    elif y >= whiteYLimit:
                        self.board[pos] = GamePiece("W", [-1])


    def validXorY(self, xOrY):
        return (xOrY < self.size) and (xOrY >= 0)


    def validPosition(self, pos):
        return self.validXorY(pos.x) and self.validXorY(pos.y)


    def validPlayerPos(self, player, pos):
        if pos in self.board:
            return self.board[pos].color == player.color
        
        return False


    # def completeJump(self, player, startPos, endPos):
    #     if (startPos.x - endPos.x) != 2:
    #         return False

    #     