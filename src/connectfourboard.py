

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