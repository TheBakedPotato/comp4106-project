#!/usr/bin/python3

from textui import TextUI
from connectfourgame import ConnectFourGame
from aiplayer import AIPlayer
from player import Player


def simpleHeuristic(player, game):
    weightPlayerOpenLines = 1
    weightPlayerForks = 1
    weightOppoentClosedOpenLines = 1
    weightOpponentForks = 1



    return 0


def horizontalOpenLine(board, xPos, yPos, lineSize):
    if (board.xSize - xPos) < lineSize:
        return None

    lineColor = None
    for newXPos in range(xPos, xPos + lineSize):
        # newXPos = xPos + (dX * direction)
        if board.hasGamePiece(newXPos, yPos) and (lineColor is None):
            lineColor = board[newXPos][yPos]
        elif board.hasGamePiece(newXPos, yPos) and (lineColor != board[newXPos][yPos]):
            return None

    return lineColor


def verticalOpenLine(board, xPos, yPos, lineSize):
    if (board.ySize - yPos) < lineSize:
        return None

    lineColor = None
    for newYPos in range(yPos, yPos + lineSize):
        if board.hasGamePiece(xPos, newYPos) and (lineColor is None):
            lineColor = board[xPos][newYPos]
        elif board.hasGamePiece(xPos, newYPos) and (lineColor != board[xPos][newYPos]):
            return None

    return lineColor


def diagonalOpenLine(board, xPos, yPos, lineSize, direction=1):
    maxX = 0
    if direction > 0:
        maxX = board.xSize - xPos
    else:
        maxX = xPos + 1
    if ((board.ySize - yPos) < lineSize) or (maxX < lineSize):
        return False

    lineColor = None
    for delta in range(0, lineSize):
        newXPos = xPos + (delta * direction)
        newYPos = yPos + delta

        if board.hasGamePiece(newXPos, newYPos) and (lineColor is None):
            lineColor = board[newXPos][newYPos]
        elif board.hasGamePiece(newXPos, newYPos) and (lineColor != board[newXPos][newYPos]):
            return None

    return lineColor


def horizontalFork(board, xPos, yPos, lineSize):
    if board.hasPiece(xPos, yPos) or ((board.xSize - xPos) < minLineSize):
        return None

    lineColor = None
    for newXPos in range(xPos + 1, xPos + lineSize):
        if board.hasPiece(newXPos, yPos):
            continue

    return lineColor

# def horizontalOpenLine(board, xPos, yPos, lineSize, direction=1):
#     color = board[xPos][yPos]
#     prevX = xPos + (-1 * direction)
#     maxRunSize = 0
#     if direction > 0:
#         maxRunSize = board.xSize - xPos
#     else:
#         maxRunSize = xPos + 1
#     if (board.hasGamePiece(prevX, yPos) and (board[prevX][yPos] == color)) or (maxRunSize < lineSize):
#         return False

#     foundEmptyTile = False
#     for dX in range(1, lineSize):
#         newXPos = xPos + (dX * direction)
#         if board.hasGamePiece(newXPos, yPos) and ((board[newXPos][yPos] != color) or foundEmptyTile):
#             return False
#         elif not board.hasGamePiece(newXPos, yPos):
#             foundEmptyTile = True

#     return True


def checkPlayerOpenLines(game):
    lineSize = 4
    playerValues = {}
    for player in game.players:
        playerValues[player.color] = 0

    for yPos in range(game.board.ySize):
        for xPos in range(game.board.xSize):
            color = None
            color = horizontalOpenLine(game.board, xPos, yPos, lineSize)
            if color:
                playerValues[color] += 1

            color = None
            color = verticalOpenLine(game.board, xPos, yPos, lineSize)
            if color:
                playerValues[color] += 1

            color = None
            color = diagonalOpenLine(game.board, xPos, yPos, lineSize)
            if color:
                playerValues[color] += 1

            color = None
            color = diagonalOpenLine(game.board, xPos, yPos, lineSize, -1)
            if color:
                playerValues[color] += 1

    return playerValues



#############################################################################################
ui = TextUI()
colors = [ "B", "W" ]
human1 = Player(colors[1])
human2 = Player(colors[0])
simpleAI = AIPlayer(colors[0], simpleHeuristic, 1)
players = [ human1, human2 ]
# players = [ human1, simpleAI ]
game = ConnectFourGame(players, 7, 6)

running = True

while running:

    player = game.getNextPlayer()
    ui.displayPlayersTurn(player)
    ui.drawBoard(game.board)
    column = player.move(game)
    if column is None:
        while column is None:
            column = ui.getColumn()
            if not game.validColumn(column):
                ui.invalidColumn(column)
                column = None

    game.applyMove(player, column)
    playerValues = checkPlayerOpenLines(game)
    for player, value in playerValues.items():
        print("Player: {}, Value: {}".format(player, value))

    if game.gameOver():
        print("Game Over")
        ui.drawBoard(game.board)
        running = False