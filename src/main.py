#!/usr/bin/python3

import random

from textui import TextUI
from connectfourgame import ConnectFourGame
from aiplayer import AIPlayer
from player import Player
from adaptiveaiplayer import AdaptiveAIPlayer
from move import Move


def gameLoop(players, ui):
    random.shuffle(players)
    game = ConnectFourGame(players, 7, 6)
    prevMove = None
    prevGame = None

    while not game.gameOver:
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
        prevMove = Move(move.player, move.column)
        game.applyMove(move)
    else:
        if game.winner is not None:
            ui.gameOverWithWinner(game.winner)
        else:
            ui.gameOverDraw()

        ui.drawBoard(game.board)





#############################################################################################
# human0 = Player(colors[0])
# human1 = Player(colors[1])
# simpleAI0 = AIPlayer(colors[0], 1)
# simpleAI1 = AIPlayer(colors[1], 1)
# mmAI0 = AIPlayer(colors[0], 5)
# mmAI1 = AIPlayer(colors[1], 5)
# ammAI0 = AdaptiveAIPlayer(colors[0], 5, 100)
# ammAI1 = AdaptiveAIPlayer(colors[1], 5, 100)
# players = [ human0 ]
# players = [ human0, human1 ]
# players = [ human0, mmAI1 ]
# players = [ human1, ammAI0 ]
# players = [ simpleAI0, simpleAI1 ]
# players = [ simpleAI0, human1 ]
# players = [ human0, simpleAI1 ]
# players = [ simpleAI0, mmAI1 ]
# players = [ simpleAI0, ammAI1 ]
# players = [ mmAI0, ammAI1 ]
# players = [ mmAI0, mmAI1 ]
# random.shuffle(players)
# game = ConnectFourGame(players, 7, 6)
# firstPlayer = players[0]




# winCount = {}
# for player in players:
#     winCount[player.color] = 0
# count = 1

colors = [ "X", "O" ]
ui = TextUI()
running = True

while running:

    option = ui.mainMenu()
    players = []
    playerTypes = []
    if option == 1:
        playerCount = 0

        while playerCount < 2:
            option = ui.pickPlayerType()
            player = None
            playerType = None
            if option == 1:
                player = Player(colors[playerCount])
                playerType = ("Human", colors[playerCount])
            elif option == 2:
                player = AIPlayer(colors[playerCount], 1)
                playerType = ("Easy", colors[playerCount])
            elif option == 3:
                player = AIPlayer(colors[playerCount], 5)
                playerType = ("Hard", colors[playerCount])
            elif option == 4:
                player = AdaptiveAIPlayer(colors[playerCount], 5, 100)
                playerType = ("Adaptive", colors[playerCount])

            playerTypes.append(playerType)
            players.append(player)
            playerCount += 1

        ui.playerSelections(playerTypes)

    elif option == 2:
        running = False

    if running:
        gameLoop(players, ui)
    # if running and (not game.gameOver):
    #     player = game.getNextPlayer()
    #     ui.displayPlayersTurn(player)
    #     ui.drawBoard(game.board)
    #     move = player.move(game, prevMove, prevGame)
    #     if move is None:
    #         column = None
    #         while column is None:
    #             column = ui.getColumn()
    #             if not game.validColumn(column):
    #                 ui.invalidColumn(column)
    #                 column = None

    #         move = Move(player, column)

    #     prevGame = game.copy()
    #     prevMove = Move(move.player, move.column)
    #     game.applyMove(move)

    # else:
    #     print("Game Over")
    #     if game.winner:
    #         print("The winner is: {}!".format(game.winner.color))
    #         winCount[game.winner.color] += 1
    #     else:
    #         print("The game was a draw!")

    #     ui.drawBoard(game.board)
    #     if count > 1:
    #         count -= 1
    #         random.shuffle(players)
    #         game = ConnectFourGame(players, 7, 6)
    #         prevMove = None
    #         prevGame = None
    #     else:
    #         running = False


# print("First Player: {}".format(firstPlayer.color))
# print("Total Games: {}".format(50))
# for player, count in winCount.items():
#     print("Player {} Won: {}".format(player, count))