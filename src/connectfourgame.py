from position import Position
from connectfourboard import ConnectFourBoard

class ConnectFourGame:

    def __init__(self, xSize, ySize):
        self.board = ConnectFourBoard(xSize, ySize)


    def validXValue(self, xValue):
        return (xValue < self.xSize) and (xValue >= 0)


    def validYValue(self, yValue):
        return (yValue < self.ySize) and (yValue >= 0)


    def validPosition(self, pos):
        return self.validXValue(pos.x) and self.validYValue(pos.y)


    def makeMove(self, column):
        for y in range(0, self.ySize):
            pos = Position(column, y)