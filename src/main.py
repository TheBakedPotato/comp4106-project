#!/usr/bin/python3

from textui import TextUI
from connectfourgame import ConnectFourGame
from aiplayer import AIPlayer
from player import Player


def simpleHeuristic(player, game):
    weightPlayerLines = 1
    weightPlayerForks = 1
    weightOppoentClosedLines = 1
    weightOpponentForks = 1



    return 0




#############################################################################################
ui = TextUI()
colors = [ "B", "W" ]
human1 = Player(colors[1])
human2 = Player(colors[0])
simpleAI = AIPlayer(colors[0], simpleHeuristic, 1)
# players = [ human1, human2 ]
players = [ human1, simpleAI ]
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

    if game.gameOver():
        print("Game Over")
        ui.drawBoard(game.board)
        running = False