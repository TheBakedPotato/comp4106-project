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


    def playerUpwardDiagonalOpenLinesCount(self, lineSize):
        playerValues = {}
        for player in self.players:
            playerValues[player.color] = 0

        if (self.board.xSize < lineSize) or (self.board.ySize < lineSize):
            return playerValues

        ################################################################################################
        # Calculating all the diagonals going up starting at row of index 1
        # Just increasing the row value
        maxRow = (self.board.ySize - lineSize)
        startColumn = 0
        for row in range(1, maxRow + 1):
            maxYDelta = self.board.ySize - row
            startDelta = 0
            lastColorDelta = 0
            currColor = None

            for delta in range(min(self.board.xSize, maxYDelta)):
                currRow = row + delta
                currColumn = startColumn + delta

                if startDelta == (delta - lineSize):
                    startDelta += 1
                elif startDelta < (delta - lineSize):
                    print("ERROR: playerDiagonalOpenLinesCount INCREMENTING DELTA FOR ROW")

                if self.board.hasGamePiece(currColumn, currRow):
                    if currColor is None:
                        currColor = self.board[currColumn][currRow]
                    elif currColor != self.board[currColumn][currRow]:
                        startDelta = max(lastColorDelta + 1, startDelta)
                        currColor = self.board[currColumn][currRow]

                    lastColorDelta = delta
                
                if currColor is not None:
                    if (delta - startDelta) == (lineSize - 1) and (lastColorDelta >= startDelta):
                        playerValues[currColor] += 1
        ################################################################################################

        ################################################################################################
        # Calculating all the diagonals going up starting at column of index 0
        # Just increasing the column value
        maxColumn = (self.board.xSize - lineSize)
        startRow = 0
        for column in range(0, maxColumn + 1):
            maxXDelta = self.board.xSize - column
            startDelta = 0
            lastColorDelta = 0
            currColor = None

            for delta in range(min(self.board.ySize, maxXDelta)):
                currColumn = column + delta
                currRow = startRow + delta

                deltaDiff = delta - lineSize
                if startDelta == deltaDiff:
                    startDelta += 1
                elif startDelta < deltaDiff:
                    print("ERROR: playerDiagonalOpenLinesCount INCREMENTING DELTA FOR COLUMN")

                if self.board.hasGamePiece(currColumn, currRow):
                    if currColor is None:
                        currColor = self.board[currColumn][currRow]
                    elif currColor != self.board[currColumn][currRow]:
                        startDelta = max(lastColorDelta + 1, startDelta)
                        currColor = self.board[currColumn][currRow]

                    lastColorDelta = delta

                if currColor is not None:
                    if (delta - startDelta) == (lineSize - 1) and (lastColorDelta >= startDelta):
                        playerValues[currColor] += 1
        ################################################################################################

        return playerValues


    def playerDownwardDiagonalOpenLinesCount(self, lineSize):
        playerValues = {}
        for player in self.players:
            playerValues[player.color] = 0

        if (self.board.xSize < lineSize) or (self.board.ySize < lineSize):
            return playerValues

        ################################################################################################
        # Calculating all the diagonals going down starting at row of index 1
        # Just increasing the row value
        maxRow = (self.board.ySize - lineSize)
        startColumn = self.board.xSize - 1
        for row in range(1, maxRow + 1):
            maxYDelta = self.board.ySize - row
            startDelta = 0
            lastColorDelta = 0
            currColor = None

            for delta in range(min(self.board.xSize, maxYDelta)):
                currColumn = startColumn - delta
                currRow = row + delta

                deltaDiff = delta - lineSize
                if startDelta == deltaDiff:
                    startDelta += 1
                elif startDelta < deltaDiff:
                    print("ERROR 1")

                if self.board.hasGamePiece(currColumn, currRow):
                    if currColor is None:
                        currColor = self.board[currColumn][currRow]
                    elif currColor != self.board[currColumn][currRow]:
                        startDelta = max(lastColorDelta + 1, startDelta)
                        currColor = self.board[currColumn][currRow]

                    lastColorDelta = delta

                if currColor is not None:
                    if (delta - startDelta) == (lineSize - 1) and (lastColorDelta >= startDelta):
                        playerValues[currColor] += 1

                # print("Curr Column: {}, Curr Row: {}".format(currColumn, currRow))
        ################################################################################################

        ################################################################################################
        # Calculating all the diagonals going down starting at column of index lineSize - 1
        # Just increasing the column value
        for column in range(lineSize - 1, self.board.xSize):
            maxXDelta = column + 1
            startDelta = 0
            lastColorDelta = 0
            currColor = None

            for delta in range(min(self.board.ySize, maxXDelta)):
                currColumn = column - delta
                currRow = delta

                deltaDiff = delta - lineSize
                if startDelta == deltaDiff:
                    startDelta += 1
                elif startDelta < deltaDiff:
                    print("ERROR 2")

                if self.board.hasGamePiece(currColumn, currRow):
                    if currColor is None:
                        currColor = self.board[currColumn][currRow]
                    elif currColor != self.board[currColumn][currRow]:
                        startDelta = max(lastColorDelta + 1, startDelta)
                        currColor = self.board[currColumn][currRow]

                    lastColorDelta = delta

                if currColor is not None:
                    if (delta - startDelta) == (lineSize - 1) and (lastColorDelta >= startDelta):
                        playerValues[currColor] += 1
        ################################################################################################

        return playerValues