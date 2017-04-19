from position import Position
from connectfourboard import ConnectFourBoard

class ConnectFourGame:

    def __init__(self, players, xSize, ySize):
        self.players = players
        self.playerIndex = 0
        self.board = ConnectFourBoard(xSize, ySize)
        self.winner = None
        self.gameOver = False


    def copy(self):
        newGame = ConnectFourGame(self.players, self.board.xSize, self.board.ySize)
        newGame.playerIndex = self.playerIndex
        newGame.board = self.board.copy()
        newGame.gameOver = self.gameOver
        newGame.winner = self.winner

        return newGame


    def validColumn(self, column):
        return self.board.validColumn(column)


    def hasHorizontalLine(self, xPos, yPos, lineSize):
        if not self.board.hasGamePiece(xPos, yPos) or (self.board.xSize - xPos) < lineSize:
            return False

        pieceColor = self.board[xPos][yPos]
        for newXPos in range(xPos + 1, xPos + lineSize):
            if not self.board.hasGamePiece(newXPos, yPos) or (self.board[newXPos][yPos] != pieceColor):
                return False

        return True


    def hasVerticalLine(self, xPos, yPos, lineSize):
        if not self.board.hasGamePiece(xPos, yPos) or (self.board.ySize - yPos) < lineSize:
            return False

        pieceColor = self.board[xPos][yPos]
        for newYPos in range(yPos + 1, yPos + lineSize):
            if not self.board.hasGamePiece(xPos, newYPos) or (self.board[xPos][newYPos] != pieceColor):
                return False

        return True


    # Direction indicates the diagonal going left or right. 1 == right, -1 == left
    def hasDiagonalLine(self, xPos, yPos, lineSize, direction=1):
        if not self.board.hasGamePiece(xPos, yPos) or (self.board.ySize - yPos) < lineSize:
            return False

        pieceColor = self.board[xPos][yPos]
        for delta in range(1, lineSize):
            newXPos = xPos + (direction * delta)
            newYPos = yPos + delta
            if not self.board.hasGamePiece(newXPos, newYPos) or (self.board[newXPos][newYPos] != pieceColor):
                return False

        return True


    def inLine(self, color, xPos, yPos, lineSize):
        horizontalCount = 1
        verticalCount = 1
        downDiagCount = 1
        upDiagCount = 1

        foundLine = False

        checkBack = True
        checkForward = True

        checkDown = True
        checkUp = True

        checkBackDown = True
        checkBackUp = True
        checkFowardDown = True
        checkForwardUp = True

        for delta in range(1, lineSize):
            noLine = True

            backX = xPos - delta
            forwardX = xPos + delta

            downY = yPos - delta
            upY = yPos + delta

            ###################################################################################################
            # Checking the existence of a horizontal line
            if checkBack and self.board.hasGamePiece(backX, yPos) and self.board[backX][yPos] == color:
                horizontalCount += 1
                noLine = False
            else:
                checkBack = False

            if checkForward and self.board.hasGamePiece(forwardX, yPos) and self.board[forwardX][yPos] == color:
                horizontalCount += 1
                noLine = False
            else:
                checkForward = False

            if horizontalCount >= lineSize:
                foundLine = True
            ####################################################################################################

            ####################################################################################################
            # Checking the existence of a vertical line
            if checkDown and self.board.hasGamePiece(xPos, downY) and self.board[xPos][downY] == color:
                verticalCount += 1
                noLine = False
            else:
                checkDown = False

            if checkUp and self.board.hasGamePiece(xPos, upY) and self.board[xPos][upY] == color:
                verticalCount += 1
                noLine = False
            else:
                checkUp = False

            if verticalCount >= lineSize:
                foundLine = True
            ####################################################################################################

            ####################################################################################################
            # Checking the existence of diagonal lines pointed foward up
            if checkBackDown and self.board.hasGamePiece(backX, downY) and self.board[backX][downY] == color:
                upDiagCount += 1
                noLine = False
            else:
                checkBackDown = False

            if checkForwardUp and self.board.hasGamePiece(forwardX, upY) and self.board[forwardX][upY] == color:
                upDiagCount += 1
                noLine = False
            else:
                checkForwardUp = False

            if upDiagCount >= lineSize:
                foundLine = True
            ####################################################################################################

            ####################################################################################################
            # Checking the existence of diagonal lines pointed foward down
            if checkBackUp and self.board.hasGamePiece(backX, upY) and self.board[backX][upY] == color:
                downDiagCount += 1
                noLine = False
            else:
                checkBackUp = False

            if checkFowardDown and self.board.hasGamePiece(forwardX, downY) and self.board[forwardX][downY] == color:
                downDiagCount += 1
                noLine = False
            else:
                checkFowardDown = False

            if downDiagCount >= lineSize:
                foundLine = True
            ####################################################################################################

            if foundLine:
                return True
            elif noLine:
                return False

        print("ERROR: CHECKING inLine")
        return False


    def isGameOver(self, move):
        lineSize = 4
        numFullColumns = 0
        for column in self.board.board:
            if len(column) == self.board.ySize:
                numFullColumns += 1

        xPos = move.column
        yPos = len(self.board[move.column]) - 1
        color = move.player.color
        if self.inLine(color, xPos, yPos, lineSize):
            self.winner = move.player
            return True
        elif numFullColumns == self.board.xSize:
            return True

        return False


    def applyMove(self, move):
        self.board[move.column].append(move.player.color)
        self.gameOver = self.isGameOver(move)


    def undoMove(self, move):
        self.board[move.column].pop()


    def getNextPlayer(self):
        nextPlayer = self.players[self.playerIndex]
        self.playerIndex += 1
        if self.playerIndex >= len(self.players):
            self.playerIndex = 0

        return nextPlayer


    def playerHorizontalOpenLinesCount(self, lineSize):
        playerValues = {}
        currColor = None
        for player in self.players:
            playerValues[player.color] = 0

        for yPos in range(self.board.ySize):
            startPos = 0
            lastColorX = 0
            currColor = None
            for xPos in range(self.board.xSize):
                if startPos == (xPos - lineSize):
                    startPos += 1
                elif startPos < (xPos - lineSize):
                    print("Something is wack")

                if self.board.hasGamePiece(xPos, yPos):
                    if currColor == None:
                        currColor = self.board[xPos][yPos]
                    elif currColor != self.board[xPos][yPos]:
                        startPos = max(lastColorX + 1, startPos)
                        currColor = self.board[xPos][yPos]

                    lastColorX = xPos

                if currColor is not None:
                    if (xPos - startPos) == (lineSize - 1) and (lastColorX >= startPos):
                        playerValues[currColor] += 1

        return playerValues


    def playerVerticalOpenLinesCount(self, lineSize):
        playerValues = {}
        for player in self.players:
            playerValues[player.color] = 0

        for columnNum in range(0, self.board.xSize):
            column = self.board[columnNum]
            columnLen = len(column)
            emptyTiles = self.board.ySize - columnLen
            if columnLen != 0 and emptyTiles > 0:
                color = self.board[columnNum][columnLen - 1]
                if emptyTiles >= (lineSize - 1):
                    playerValues[color] += 1
                else:
                    lastIndex = columnLen - (lineSize - emptyTiles)
                    line = True
                    for row in range(columnLen - 2, lastIndex - 1, -1):
                        if self.board[columnNum][row] != color:
                            line = False
                            break

                    if line:
                        playerValues[color] += 1

        return playerValues


    # def checkPlayerForks(self):
    #     forkMaxSize = 5
    #     forkMinSize = 4
    #     playerValues = {}
    #     for player in self.players:
    #         playerValues[player.color] = 0

    #     for yPos in range(self.board.ySize):
    #         for xPos in range(self.board.xSize):
    #             color = None
    #             color = self.board.horizontalFork(xPos, yPos, forkMaxSize, forkMinSize)
    #             if color:
    #                 playerValues[color] += 1

    #             # color = None
    #             # color = self.board.diagonalFork(xPos, yPos, forkMaxSize, forkMinSize)
    #             # if color:
    #             #     playerValues[color] += 1

    #             # color = None
    #             # color = self.board.diagonalFork(xPos, yPos, forkMaxSize, forkMinSize, -1)
    #             # if color:
    #             #     playerValues[color] += 1

    #     return playerValues