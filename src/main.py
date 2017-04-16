#!/usr/bin/python3

from textui import TextUI
from connectfourgame import ConnectFourGame
from aiplayer import AIPlayer
from player import Player

ui = TextUI()
colors = ["B", "W"]
game = ConnectFourGame(7, 6)
# ai = AIPlayer(colors[0])
human1 = Player(colors[1])
human2 = Player(colors[0])


running = True

while running:
    ui.drawBoard(game.board)

    column = None
    while column is None:
        column = ui.getColumn()
        if not game.validColumn(column):
            ui.invalidColumn(column)
            column = None

    game.applyMove(human1, column)

    if game.gameOver():
        print("Game Over")

    # ui.drawBoard(game.board)

    # column = None
    # while column is None:
    #     column = ui.getColumn()
    #     if not game.validColumn(column):
    #         ui.invalidColumn(column)
    #         column = None

    # game.applyMove(human2, column)
