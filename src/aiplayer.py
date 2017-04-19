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


    def simpleHeuristic(self, game):
        if game.gameOver:
            if game.winner is not None and game.winner == self:
                return float("inf")
            else:
                return float("-inf")

        lineSize = 4

        horizontalCounts = game.playerHorizontalOpenLinesCount(lineSize)
        verticalCounts = game.playerVerticalOpenLinesCount(lineSize)
        upwardDiagonalCounts = game.playerUpwardDiagonalOpenLinesCount(lineSize)
        downwardDiagonalCounts = game.playerDownwardDiagonalOpenLinesCount(lineSize)


        value = horizontalCounts[self.color]
        value += verticalCounts[self.color]
        value += upwardDiagonalCounts[self.color]
        value += downwardDiagonalCounts[self.color]
        for player in game.players:
            if player != self:
                value -= horizontalCounts[player.color]
                value -= verticalCounts[player.color]
                value -= upwardDiagonalCounts[player.color]
                value -= downwardDiagonalCounts[player.color]

        return value

    
    def maxValue(self, game, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return self.simpleHeuristic(game)

        value = float("-inf")
        moves = self.productionSystem(game)
        random.shuffle(moves)
        for currMove in moves:
            currGame = game.copy()
            currGame.applyMove(currMove)
            value = max(value, self.minValue(currGame, depth - 1, alpha, beta))
            if value >= beta:
                return value

            alpha = max(value, alpha)

        return value


    def minValue(self, game, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return self.simpleHeuristic(game)

        value = float("inf")
        for playerIndex in range(len(game.players)):
            if game.players[playerIndex] != self:
                moves = self.productionSystem(game, game.players[playerIndex])
                random.shuffle(moves)
                for currMove in moves:
                    currGame = game.copy()
                    currGame.applyMove(currMove)
                    value = min(value, self.maxValue(currGame, depth - 1, alpha, beta))
                    if value <= alpha:
                        return value

                    beta = min(value, beta)

        return value


    def move(self, game):
        move = None
        
        alpha = float("-inf")
        beta = float("inf")

        value = float("-inf")
        moves = self.productionSystem(game)
        random.shuffle(moves)
        for currMove in moves:
            currGame = game.copy()
            currGame.applyMove(currMove)
            currVal = self.minValue(currGame, self.searchDepth - 1, alpha, beta)
            if (move is None) or (currVal > value):
                move = currMove
                value = currVal

            alpha = max(value, alpha)

        currGame = game.copy()
        currGame.applyMove(move)

        return move