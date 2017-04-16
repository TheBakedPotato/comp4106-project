from texttable import Texttable

from position import Position

class TextUI:

    def __init__(self):
        pass

    def drawBoard(self, board):
        textBoard = Texttable()
        header = [""]
        for i in range(board.size):
            header.append(i)

        textBoard.header(header)

        for y in range(board.size):
            newRow = [y]
            for x in range(board.size):
                pos = Position(x,y)
                if pos in board.board:
                    newRow.append(board.board[pos].color)
                else:
                    newRow.append("")

            textBoard.add_row(newRow)

        return textBoard


    def getPos(self, startOrEnd):
        pos = None

        while pos is None:
            try:
                data = input("Enter the {} pos: ".format(startOrEnd))
                pos = tuple(int(x.strip()) for x in data.split(','))
            except ValueError:
                self.invalidInput(data)
                pos = None
        
        return Position(pos[0], pos[1])


    def getStartPos(self):
        return self.getPos("Start")


    def getEndPos(self):
        return self.getPos("End")


    def invalidInput(self, data):
        print("{} is an invalid input. Please try again.".format(data))


    def invalidPosition(self, pos):
        print("{} is an invalid position. Please try again".format((pos.x, pos.y)))

