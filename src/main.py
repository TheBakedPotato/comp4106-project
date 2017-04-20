#!/usr/bin/python3

import random

from textui import TextUI
from connectfourgame import ConnectFourGame
from aiplayer import AIPlayer
from player import Player
from adaptiveaiplayer import AdaptiveAIPlayer
from move import Move


#############################################################################################
ui = TextUI()
colors = [ "X", "O" ]
human0 = Player(colors[0])
human1 = Player(colors[1])
simpleAI0 = AIPlayer(colors[0], 1)
simpleAI1 = AIPlayer(colors[1], 1)
mmAI0 = AIPlayer(colors[0], 5)
mmAI1 = AIPlayer(colors[1], 5)
ammAI0 = AdaptiveAIPlayer(colors[0], 5, 100)
ammAI1 = AdaptiveAIPlayer(colors[1], 5, 100)
# players = [ human0 ]
# players = [ human0, human1 ]
# players = [ human0, mmAI1 ]
# players = [ human1, ammAI0 ]
# players = [ simpleAI0, simpleAI1 ]
# players = [ simpleAI0, human1 ]
# players = [ simpleAI0, mmAI1 ]
players = [ simpleAI0, ammAI1 ]
# players = [ mmAI0, ammAI1 ]
# players = [ mmAI0, mmAI1 ]
random.shuffle(players)
game = ConnectFourGame(players, 7, 6)


running = True
prevMove = None
prevGame = None

winCount = {}
for player in players:
    winCount[player.color] = 0
count = 1

while running:

    if not game.gameOver:
        player = game.getNextPlayer()
        ui.displayPlayersTurn(player)
        ui.drawBoard(game.board)
        move = player.move(game, prevMove, prevGame)
        if move is None:
            column = None
            while column is None:
                column = ui.getColumn()
                if not game.validColumn(column):
                    ui.invalidColumn(column)
                    column = None

            move = Move(player, column)

        prevGame = game.copy()
        game.applyMove(move)
        prevMove = Move(move.player, move.column)

    else:
        # print("Game Over")
        if game.winner:
            # print("The winner is: {}!".format(game.winner.color))
            winCount[game.winner.color] += 1
        # else:
        #     print("The game was a draw!")

        ui.drawBoard(game.board)
        if count > 1:
            count -= 1
        else:
            running = False

        random.shuffle(players)
        game = ConnectFourGame(players, 7, 6)
        prevMove = None
        prevGame = None

print("Total Games: {}".format(50))
for player, count in winCount.items():
    print("Player {} Won: {}".format(player, count))
# print("First Player: {}".format(players[0].color))