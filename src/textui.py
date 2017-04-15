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
                    newRow.append(board.board[pos])
                else:
                    newRow.append("")

            textBoard.add_row(newRow)

        return textBoard