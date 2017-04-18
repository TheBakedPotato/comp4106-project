#!/usr/bin/python3

from textui import TextUI
from connectfourgame import ConnectFourGame
from aiplayer import AIPlayer
from player import Player
from move import Move


#############################################################################################
ui = TextUI()
colors = [ "X", "O" ]
human0 = Player(colors[0])
human1 = Player(colors[1])
simpleAI0 = AIPlayer(colors[0], 1)
simpleAI1 = AIPlayer(colors[1], 1)
mmAI1 = AIPlayer(colors[1], 10)
# players = [ human0, human1 ]
# players = [ human0, mmAI ]
# players = [ simpleAI0, human1 ]
players = [ simpleAI0, simpleAI1 ]
# players = [ simpleAI0, mmAI1 ]
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