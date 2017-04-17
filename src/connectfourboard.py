

class ConnectFourBoard:

    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.board = []
        for i in range(0, self.xSize):
            self.board.append([])


    def copy(self):
        newBoard = ConnectFourBoard(self.xSize, self.ySize)
        for column in range(0, self.xSize):
            for row in range(0, self.ySize):
                if self.hasGamePiece(column, row):
                    newBoard.board[column].append(self.board[column][row])

        return newBoard


    def __getitem__(self, index):
        return self.board[index]


    def validYValue(self, yValue):
        return yValue >= 0 and yValue < self.ySize


    def validXValue(self, xValue):
        return xValue >= 0 and xValue < self.xSize


    def validColumn(self, column):
        if self.validXValue(column):
            return len(self.board[column]) < self.ySize

        return False


    def hasGamePiece(self, xPos, yPos):
        if self.validXValue(xPos) and self.validYValue(yPos):
            return len(self.board[xPos]) > yPos

        return False


    ##############################################
    # Functions for finding open lines and forks #
    ##############################################
    def horizontalOpenLine(self, xPos, yPos, lineSize):
        if (self.xSize - xPos) < lineSize:
            return None

        lineColor = None
        for newXPos in range(xPos, xPos + lineSize):
            if self.hasGamePiece(newXPos, yPos) and (lineColor is None):
                lineColor = self.board[newXPos][yPos]
            elif self.hasGamePiece(newXPos, yPos) and (lineColor != self.board[newXPos][yPos]):
                return None

        return lineColor


    def verticalOpenLine(self, xPos, yPos, lineSize):
        if (self.ySize - yPos) < lineSize:
            return None

        lineColor = None
        for newYPos in range(yPos, yPos + lineSize):
            if self.hasGamePiece(xPos, newYPos) and (lineColor is None):
                lineColor = self.board[xPos][newYPos]
            elif self.hasGamePiece(xPos, newYPos) and (lineColor != self.board[xPos][newYPos]):
                return None

        return lineColor


    def diagonalOpenLine(self, xPos, yPos, lineSize, direction=1):
        maxX = 0
        if direction > 0:
            maxX = self.xSize - xPos
        else:
            maxX = xPos + 1
        if ((self.ySize - yPos) < lineSize) or (maxX < lineSize):
            return False

        lineColor = None
        for delta in range(0, lineSize):
            newXPos = xPos + (delta * direction)
            newYPos = yPos + delta

            if self.hasGamePiece(newXPos, newYPos) and (lineColor is None):
                lineColor = self.board[newXPos][newYPos]
            elif self.hasGamePiece(newXPos, newYPos) and (lineColor != self.board[newXPos][newYPos]):
                return None

        return lineColor


    def horizontalFork(self, xPos, yPos, forkMaxSize, forkMinSize):
        if self.hasGamePiece(xPos, yPos) or ((self.xSize - xPos) < forkMinSize):
            return None

        lineColor = None
        for delta in range(1, forkMaxSize):
            newXPos = xPos + delta
            if self.hasGamePiece(newXPos, yPos):
                if lineColor is None:
                    lineColor = self.board[newXPos][yPos]
                elif lineColor != self.board[newXPos][yPos]:
                    return None
            elif not (delta >= (forkMinSize - 1) and delta <= (forkMaxSize - 1)):
                return None

        return lineColor


    # def verticalFork(self, xPos, yPos, forkMaxSize, forkMinSize):
    #     if self.hasGamePiece(xPos, yPos) or ((self.ySize - yPos) < forkMinSize):
    #         return None

    #     lineColor = None
    #     for delta in range(1, forkMaxSize):
    #         newYPos = yPos + delta
    #         if self.hasGamePiece(xPos, newYPos):
    #             if lineColor is None:
    #                 lineColor = self.board[xPos][newYPos]
    #             elif lineColor != self.board[xPos][newYPos]:
    #                 return None
    #         elif not (delta >= (forkMinSize - 1) and delta <= (forkMaxSize - 1)):
    #             return None

    #     return lineColor


    def diagonalFork(self, xPos, yPos, forkMaxSize, forkMinSize, direction=1):
        maxX = 0
        if direction > 0:
            maxX = self.xSize - xPos
        else:
            maxX = xPos + 1
        if self.hasGamePiece(xPos, yPos) or ((self.ySize - yPos) < forkMinSize) or (maxX < forkMinSize):
            return None

        lineColor = None
        for delta in range(1, forkMaxSize):
            newXPos = xPos + (delta * direction)
            newYPos = yPos + delta
            if self.hasGamePiece(newXPos, newYPos):
                if lineColor is None:
                    lineColor = self.board[newXPos][newYPos]
                elif lineColor != self.board[newXPos][newYPos]:
                    return None
            elif not (delta >= (forkMinSize - 1) and delta <= (forkMaxSize - 1)):
                return None

        return lineColor


