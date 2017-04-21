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


    def mainMenu(self):
        option = None

        while option is None:
            try:
                print("Please make a selection:")
                print("Play a Game - 1")
                print("Quit        - 2")
                raw = input("Your Selection: ")
                option = int(raw)
            except ValueError:
                self.invalidInput(raw)
                option = None

        return option

    def pickPlayerType(self):
        option = None

        while option is None:
            try:
                print("Human Player    - 1")
                print("Easy Player     - 2")
                print("Hard Player     - 3")
                print("Adaptive Player - 4")
                raw = input("Your Selection: ")
                option = int(raw)
            except ValueError:
                self.invalidInput(raw)
                option = None

        return option

    def playerSelections(self, playerTypes):
        for player in playerTypes:
            print("Player: {}, Color: {}".format(player[0], player[1]))


    def gameOverWithWinner(self, player):
        print("Game Over")
        print("WINNER: {}".format(player.color))


    def gameOverDraw(self):
        print("Game Over")
        print("DRAW!")


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


    def displayPlayersTurn(self, player):
        print("{}'s TURN".format(player.color))

