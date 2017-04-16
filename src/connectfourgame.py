from position import Position
from connectfourboard import ConnectFourBoard

class ConnectFourGame:

    def __init__(self, xSize, ySize):
        self.board = ConnectFourBoard(xSize, ySize)


    def validColumn(self, column):
        return len(self.board[column]) < self.board.ySize


    def hasHorizontalRow(self, xPos, yPos, rowSize):
        if not self.board.hasGamePiece(xPos, yPos) or (self.board.xSize - xPos) < rowSize:
            return False

        pieceColor = self.board[xPos][yPos]
        for newXPos in range(xPos + 1, xPos + rowSize):
            if not self.board.hasGamePiece(newXPos, yPos) or (self.board[newXPos][yPos] != pieceColor):
                return False

        return True


    def hasVerticalRow(self, xPos, yPos):
        pass


    def gameOver(self):
        # MAYBE PUT THIS AS CLASS ATTRIBUTE?
        rowSize = 4
        ####################################

        numFullColumns = 0
        for column in self.board.board:
            if len(column) == self.board.ySize:
                numFullColumns += 1

        if numFullColumns == self.board.xSize:
            return True

        gameOver = False

        for y in range(self.board.ySize):
            for x in range(self.board.xSize):
                gameOver = gameOver or self.hasHorizontalRow(x, y, rowSize)
                if (len(self.board[x]) - y - 1) > 4:
                    gameOver = gameOver or self.hasVerticalRow(x, y)

        return gameOver


    def applyMove(self, player, column):
        self.board[column].append(player.color)