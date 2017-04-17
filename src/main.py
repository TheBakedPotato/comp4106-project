#!/usr/bin/python3

from textui import TextUI
from connectfourgame import ConnectFourGame
from aiplayer import AIPlayer
from player import Player
from move import Move


#############################################################################################
ui = TextUI()
colors = [ "B", "W" ]
human1 = Player(colors[1])
human2 = Player(colors[0])
simpleAI = AIPlayer(colors[0], 1)
# players = [ human1, human2 ]
players = [ human1, simpleAI ]
game = ConnectFourGame(players, 7, 6)

running = True

while running:

    if not game.gameOver:
        player = game.getNextPlayer()
        ui.displayPlayersTurn(player)
        ui.drawBoard(game.board)
        move = player.move(game)
        if move is None:
            column = None
            while column is None:
                column = ui.getColumn()
                if not game.validColumn(column):
                    ui.invalidColumn(column)
                    column = None

            move = Move(player, column)

        game.applyMove(move)
        # playerValues = game.checkPlayerOpenLines()
        # print("PLAYER OPEN LINE VALUES")
        # for player, value in playerValues.items():
        #     print("Player: {}, Value: {}".format(player, value))

        # print("PLAYER FORK VALUES")
        # playerValues = game.checkPlayerForks()
        # for player, value in playerValues.items():
        #     print("Player: {}, Value: {}".format(player, value))

    else:
        print("Game Over")
        if game.winner:
            print("The winner is: {}!".format(game.winner.color))
        else:
            print("The game was a draw!")

        ui.drawBoard(game.board)
        running = False