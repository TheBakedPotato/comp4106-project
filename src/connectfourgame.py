from position import Position
from connectfourboard import ConnectFourBoard

class ConnectFourGame:

    def __init__(self, xSize, ySize):
        self.board = ConnectFourBoard(xSize, ySize)


    def validColumn(self, column):
        return self.board.validColumn(column)


    def hasHorizontalLine(self, xPos, yPos, lineSize):
        if not self.board.hasGamePiece(xPos, yPos) or (self.board.xSize - xPos) < lineSize:
            return False

        pieceColor = self.board[xPos][yPos]
        for newXPos in range(xPos + 1, xPos + lineSize):
            if not self.board.hasGamePiece(newXPos, yPos) or (self.board[newXPos][yPos] != pieceColor):
                return False

        return True


    def hasVerticalLine(self, xPos, yPos, lineSize):
        if not self.board.hasGamePiece(xPos, yPos) or (self.board.ySize - yPos) < lineSize:
            return False

        pieceColor = self.board[xPos][yPos]
        for newYPos in range(yPos + 1, yPos + lineSize):
            if not self.board.hasGamePiece(xPos, newYPos) or (self.board[xPos][newYPos] != pieceColor):
                return False

        return True


    # Direction indicates the diagonal going left or right. 1 == right, -1 == left
    def hasDiagonalLine(self, xPos, yPos, lineSize, direction=1):
        if not self.board.hasGamePiece(xPos, yPos) or (self.board.ySize - yPos) < lineSize:
            return False

        pieceColor = self.board[xPos][yPos]
        for delta in range(1, lineSize):
            newXPos = xPos + (direction * delta)
            newYPos = yPos + delta
            if not self.board.hasGamePiece(newXPos, newYPos) or (self.board[newXPos][newYPos] != pieceColor):
                return False

        return True


    def gameOver(self):
        # MAYBE PUT THIS AS CLASS ATTRIBUTE?
        lineSize = 4
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
                gameOver = gameOver or self.hasHorizontalLine(x, y, lineSize)
                gameOver = gameOver or self.hasVerticalLine(x, y, lineSize)
                # Checks diagonal lines up and right
                gameOver = gameOver or self.hasDiagonalLine(x, y, lineSize)
                # Checks diagonal lines up and left
                gameOver = gameOver or self.hasDiagonalLine(x, y, lineSize, -1)
                if gameOver:
                    return True

        return False


    def applyMove(self, player, column):
        self.board[column].append(player.color)