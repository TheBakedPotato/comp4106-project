

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


    def hasGamePiece(self, xPos, yPos):
        if self.validXValue(xPos) and self.validYValue(yPos):
            return len(self.board[xPos]) > yPos

        return False