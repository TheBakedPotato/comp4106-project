from texttable import Texttable

from position import Position

class TextUI:

    def __init__(self):
        pass

    def drawBoard(self, board):
        textBoard = Texttable()
        header = []
        for i in range(board.xSize):
            header.append(i)

        textBoard.header(header)
        rows = []

        for tableRow in range(board.ySize):
            rows.append([])
            boardRow = board.ySize - tableRow - 1
            for x in range(board.xSize):
                currColumn = board[x]
                value = ""
                if len(currColumn) > boardRow:
                    value = currColumn[boardRow]
                rows[tableRow].append(value)

        for row in rows:
            textBoard.add_row(row)

        print(textBoard.draw())


    def getColumn(self):
        column = None

        while column is None:
            try:
                data = input("Enter the column number: ")
                column = int(data)
            except ValueError:
                self.invalidInput(data)
                column = None
        
        return column


    def invalidInput(self, data):
        print("{} is an invalid input. Please try again.".format(data))


    def invalidColumn(self, column):
        print("{} is an invalid column. Please try again".format(column))

