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


    # def isGameOver(self):
    #     # MAYBE PUT THIS AS CLASS ATTRIBUTE?
    #     lineSize = 4
    #     ####################################

    #     numFullColumns = 0
    #     for column in self.board.board:
    #         if len(column) == self.board.ySize:
    #             numFullColumns += 1

    #     if numFullColumns == self.board.xSize:
    #         return True

    #     gameOver = False

    #     for y in range(self.board.ySize):
    #         for x in range(self.board.xSize):
    #             gameOver = gameOver or self.hasHorizontalLine(x, y, lineSize)
    #             gameOver = gameOver or self.hasVerticalLine(x, y, lineSize)
    #             # Checks diagonal lines up and right
    #             gameOver = gameOver or self.hasDiagonalLine(x, y, lineSize)
    #             # Checks diagonal lines up and left
    #             gameOver = gameOver or self.hasDiagonalLine(x, y, lineSize, -1)
    #             if gameOver:
    #                 for player in self.players:
    #                     if player.color == self.board[x][y]:
    #                         self.winner = player
    #                 return True

    #     return False

    def inHorizontalLine(self, color, xPos, yPos, lineSize):
        checkBack = True
        checkForward = True
        lineCount = 1
        for delta in range(1, lineSize):
            backX = xPos - delta
            forwardX = xPos + delta

            if checkBack and self.board.hasGamePiece(backX, yPos) and self.board[backX][yPos] == color:
                lineCount += 1
            else:
                checkBack = False

            if checkForward and self.board.hasGamePiece(forwardX, yPos) and self.board[forwardX][yPos] == color:
                lineCount += 1
            else:
                checkForward = False

            if lineCount >= lineSize:
                return True
            elif not (checkBack or checkForward):
                return False

        print("ERROR: CHECKING inHorizontalLine")
        return False


    def inVerticalLine(self, color, xPos, yPos, lineSize):
        checkDown = True
        checkUp = True
        lineCount = 1
        for delta in range(1, lineSize):
            downY = yPos - delta
            upY = yPos + delta

            if checkDown and self.board.hasGamePiece(xPos, downY) and self.board[xPos][downY] == color:
                lineCount += 1
            else:
                checkDown = False

            if checkUp and self.board.hasGamePiece(xPos, upY) and self.board[xPos][upY] == color:
                lineCount += 1
            else:
                checkUp = False

            if lineCount >= lineSize:
                return True
            elif not (checkDown or checkUp):
                return False

        print("ERROR: CHECKING inVerticalLine")
        return False


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
        # if self.inHorizontalLine(color, xPos, yPos, lineSize) or self.inVerticalLine(color, xPos, yPos, lineSize):
        if self.inLine(color, xPos, yPos, lineSize):
            self.winner = move.player
            return True
        elif numFullColumns == self.board.xSize:
            return True

        return False


    def applyMove(self, move):
        self.board[move.column].append(move.player.color)
        # self.gameOver = self.isGameOver()
        self.gameOver = self.isGameOver(move)


    def undoMove(self, move):
        self.board[move.column].pop()


    def getNextPlayer(self):
        nextPlayer = self.players[self.playerIndex]
        self.playerIndex += 1
        if self.playerIndex >= len(self.players):
            self.playerIndex = 0

        return nextPlayer


    def checkPlayerOpenLines(self):
        lineSize = 4
        playerValues = {}
        for player in self.players:
            playerValues[player.color] = 0

        for yPos in range(self.board.ySize):
            for xPos in range(self.board.xSize):
                color = None
                color = self.board.horizontalOpenLine(xPos, yPos, lineSize)
                if color:
                    playerValues[color] += 1

                color = None
                color = self.board.verticalOpenLine(xPos, yPos, lineSize)
                if color:
                    playerValues[color] += 1

                color = None
                color = self.board.diagonalOpenLine(xPos, yPos, lineSize)
                if color:
                    playerValues[color] += 1

                color = None
                color = self.board.diagonalOpenLine(xPos, yPos, lineSize, -1)
                if color:
                    playerValues[color] += 1

        return playerValues


    def checkPlayerForks(self):
        forkMaxSize = 5
        forkMinSize = 4
        playerValues = {}
        for player in self.players:
            playerValues[player.color] = 0

        for yPos in range(self.board.ySize):
            for xPos in range(self.board.xSize):
                color = None
                color = self.board.horizontalFork(xPos, yPos, forkMaxSize, forkMinSize)
                if color:
                    playerValues[color] += 1

                # color = None
                # color = self.board.diagonalFork(xPos, yPos, forkMaxSize, forkMinSize)
                # if color:
                #     playerValues[color] += 1

                # color = None
                # color = self.board.diagonalFork(xPos, yPos, forkMaxSize, forkMinSize, -1)
                # if color:
                #     playerValues[color] += 1

        return playerValues