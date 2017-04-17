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


def horizontalOpenLine(board, xPos, yPos, lineSize, direction=1):
    # prevX = xPos + (-1 * direction)
    maxRunSize = 0
    if direction > 0:
        maxRunSize = board.xSize - xPos
    else:
        maxRunSize = xPos + 1
    if maxRunSize < lineSize:
        return False

    lineColor = None
    for dX in range(0, lineSize):
        newXPos = xPos + (dX * direction)
        # if board.hasGamePiece(newXPos, yPos) and ((board[newXPos][yPos] != color) or foundEmptyTile):
        if board.hasGamePiece(newXPos, yPos) and lineColor is None:
            lineColor = board[newXPos][yPos]
        elif board.hasGamePiece(newXPos, yPos) and (lineColor != board[newXPos][yPos]):
            return None

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
    playerValues = {}
    for player in game.players:
        playerValues[player.color] = 0

    for yPos in range(game.board.ySize):
        for xPos in range(game.board.xSize):
            # if game.board.hasGamePiece(xPos, yPos):
            color = None
            color = horizontalOpenLine(game.board, xPos, yPos, 4)
            if color:
                playerValues[color] += 1
            # if horizontalOpenLine(game.board, xPos, yPos, 4, -1):
            #     playerValues[color] += 1

    return playerValues


# def checkPlayerLinesAndForks(game):
#     playerValues = {}
#     checkPositions = set()

#     for lineSize in range(3, 1, -1):
#         for yPos in game.board.ySize:
#             for xPos in game.board.xSize:
#                 if game.board.hasPiece(xPos, yPos) and (xPos, yPos) not in checkPositions:
#                     checkPositions.add((xPos, yPos))
#                     # if game.hasHorizontalLine(xPos, yPos, lineSize)


#     return playerValues



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