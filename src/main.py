#!/usr/bin/python3

from textui import TextUI
from checkersboard import CheckersBoard
from aiplayer import AIPlayer
from player import Player

ui = TextUI()
colors = ["B", "W"]
board = CheckersBoard(8, colors)
ai = AIPlayer(colors[0])
human = Player(colors[1])


running = True

while running:
    textBoard = ui.drawBoard(board)
    print(textBoard.draw())

    moves = board.playerMoves(human)
    for move in moves:
        print("Start {}, End {}".format(move.startPos, move.endPos))

    # startPos = ui.getStartPos()

    # if board.validPlayerPos(human, startPos):
    #     print("Valid Selection")
    # else:
    #     ui.invalidPosition(startPos)

    # endPos = ui.getEndPos()

    # moves = ai.productionSystem(board)
    # for move in moves:
    #     print("Start Pos: {}, End Pos: {}".format(move.startPos, move.endPos))

    running = False