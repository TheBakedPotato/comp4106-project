from texttable import Texttable

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
                pos = (x,y)
                if pos in board.board:
                    newRow.append(board.board[pos])
                else:
                    newRow.append("e")

            textBoard.add_row(newRow)

        return textBoard