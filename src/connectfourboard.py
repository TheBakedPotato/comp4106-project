

class ConnectFourBoard:

    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.board = []
        for i in range(0, self.xSize):
            self.board.append([])