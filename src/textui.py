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
        for y in range(0, board.ySize):
            rows.append([])

        # Iterating through the columns in reverse
        for y in range(board.ySize - 1, -1, -1):
            rowNum = board.ySize - y - 1
            for x in range(board.xSize):
                currColumn = board.board[x]
                value = ""
                if len(currColumn) >= (y + 1):
                    value = currColumn[rowNum]

                rows[y].append(value)

        for row in rows:
            textBoard.add_row(row)

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

