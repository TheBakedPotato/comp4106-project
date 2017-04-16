from position import Position
from connectfourboard import ConnectFourBoard

class ConnectFourGame:

    def __init__(self, xSize, ySize):
        self.board = ConnectFourBoard(xSize, ySize)


    def validColumn(self, column):
        return len(self.board[column]) < self.board.ySize


    def hasHorizontalRow(self, xPos, yPos):
        pieceColor = self.board[xPos][yPos]
        for newXPos in range(xPos + 1, xPos + 4):
            if len(self.board[newXPos]) == 0 or (newXPos >= self.board.xSize) or (self.board[newXPos][yPos] != pieceColor):
                return False

        return True


    def hasVerticalRow(self, xPos, yPos):
        if len(self.board[xPos]) == 0:
            return False


    def gameOver(self):
        numFullColumns = 0
        for column in self.board.board:
            if len(column) == self.board.ySize:
                numFullColumns += 1

        if numFullColumns == self.board.xSize:
            return True

        for y in range(self.board.ySize):
            for x in range(self.board.xSize):
                if len(self.board[x]) > y:
                    return self.hasHorizontalRow(x, y)

        return False


    def applyMove(self, player, column):
        self.board[column].append(player.color)