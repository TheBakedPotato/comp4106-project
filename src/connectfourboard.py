

class ConnectFourBoard:

    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.board = []
        for i in range(0, self.xSize):
            self.board.append([])
        # self.board.append("SELPPA")
        # self.board.append("DEZZUB")
        # self.board.append("EZLLUP")


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


    def horizontalFork(self, xPos, yPos, lineSize, minSize):
        if self.hasPiece(xPos, yPos) or ((self.xSize - xPos) < minSize):
            return None

        lineColor = None
        for delta in range(1, lineSize):
            newXPos = xPos + delta
            if self.hasPiece(newXPos, yPos):
                if lineColor is None:
                    lineColor = self.board[newXPos][yPos]
                elif lineColor != self.board[newXPos][yPos]:
                    return None
            else:
                if (delta != minSize) or (delta != lineSize):
                    return None

        return lineColor


    def checkPlayerOpenLines(self):
        lineSize = 4
        playerValues = {}

        for yPos in range(self.ySize):
            for xPos in range(self.xSize):
                color = None
                color = self.horizontalOpenLine(xPos, yPos, lineSize)
                if color:
                    if color not in playerValues:
                        playerValues[color] = 0
                    playerValues[color] += 1

                color = None
                color = self.verticalOpenLine(xPos, yPos, lineSize)
                if color:
                    if color not in playerValues:
                        playerValues[color] = 0
                    playerValues[color] += 1

                color = None
                color = self.diagonalOpenLine(xPos, yPos, lineSize)
                if color:
                    if color not in playerValues:
                        playerValues[color] = 0
                    playerValues[color] += 1

                color = None
                color = self.diagonalOpenLine(xPos, yPos, lineSize, -1)
                if color:
                    if color not in playerValues:
                        playerValues[color] = 0
                    playerValues[color] += 1

        return playerValues
