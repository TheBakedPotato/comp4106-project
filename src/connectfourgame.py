from position import Position
from connectfourboard import ConnectFourBoard

class ConnectFourGame:

    def __init__(self, xSize, ySize):
        self.board = ConnectFourBoard(xSize, ySize)


    def validColumn(self, column):
        return len(self.board[column]) < self.board.ySize


    def applyMove(self, player, column):
        self.board[column].append(player.color)