import random

from player import Player
from move import Move
from position import Position

class AIPlayer(Player):

    def __init__(self, color, searchDepth):
        super().__init__(color)
        self.searchDepth = searchDepth


    def productionSystem(self, game, player=None):
        moves = []
        if player is None:
            player = self

        for column in range(game.board.xSize):
            if game.validColumn(column):
                moves.append(Move(player, column))

        return moves


    def simpleHeuristic(self, game, oldOpenLineValues):
        # if game.gameOver and game.winner == self:
        #     return float("inf")

        weightPlayerOpenLines = 1
        weightOppoentOpenLines = 5
        weightForks = 5

        playerLines = 0
        closedOpponentLines = 0
        playerForks = 0
        opponentForks = 0

        openLineValues = game.checkPlayerOpenLines()
        forkValues = game.checkPlayerForks()

        for player in game.players:
            if self == player:
                playerLines += openLineValues[self.color]
                playerForks += forkValues[self.color]
            else:
                opponentForks += forkValues[player.color]
                closedOpponentLines = oldOpenLineValues[player.color] - openLineValues[player.color]

        return (weightPlayerOpenLines * playerLines) \
               + (weightForks * playerForks) \
               + (weightOppoentOpenLines * closedOpponentLines) \
               - (weightForks * opponentForks)

    
    def maxValue(self, game, oldOpenLineValues, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return self.simpleHeuristic(game, oldOpenLineValues)

        value = float("-inf")
        oldOpenLineValues = game.checkPlayerOpenLines()
        moves = self.productionSystem(game)
        random.shuffle(moves)
        for currMove in moves:
            currGame = game.copy()
            currGame.applyMove(currMove)
            value = max(value, self.minValue(currGame, oldOpenLineValues, depth - 1, alpha, beta))
            if value >= beta:
                return value

            alpha = max(value, alpha)

        return value


    def minValue(self, game, oldOpenLineValues, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return self.simpleHeuristic(game, oldOpenLineValues)

        value = float("inf")
        for playerIndex in range(len(game.players)):
            if game.players[playerIndex] != self:
                oldOpenLineValues = game.checkPlayerOpenLines()
                moves = self.productionSystem(game, game.players[playerIndex])
                random.shuffle(moves)
                for currMove in moves:
                    currGame = game.copy()
                    currGame.applyMove(currMove)
                    value = min(value, self.maxValue(currGame, oldOpenLineValues, depth - 1, alpha, beta))
                    if value <= alpha:
                        return value

                    beta = min(value, beta)

        return value


    def move(self, game):
        move = None
        
        alpha = float("-inf")
        beta = float("inf")

        value = float("-inf")
        oldOpenLineValues = game.checkPlayerOpenLines()
        moves = self.productionSystem(game)
        random.shuffle(moves)
        for currMove in moves:
            currGame = game.copy()
            currGame.applyMove(currMove)
            currVal = self.minValue(currGame, oldOpenLineValues, self.searchDepth - 1, alpha, beta)
            if move is None:
                move = currMove
                value = currVal
            elif currVal > value:
                value = currVal
                move = currMove
            # currVal = self.simpleHeuristic(self, currGame, oldOpenLineValues)
            # print("CurrMove: {}, CurrVal: {}".format(currMove, currVal))

            # if currVal > value:
            #     value = currVal
            #     move = currMove

        # print("value: {}".format(value))
        return move
