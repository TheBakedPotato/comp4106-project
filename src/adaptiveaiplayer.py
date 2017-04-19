import random
from queue import PriorityQueue

from player import Player
from move import Move
from entry import Entry

class AdaptiveAIPlayer(Player):

    def __init__(self, color, searchDepth, maxHeuristicValue):
        super().__init__(color)
        self.searchDepth = searchDepth
        self.maxHeuristicValue = maxHeuristicValue
        self.opponentRank = -1


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
        moveScores = PriorityQueue()

        alpha = float("-inf")
        beta = float("inf")

        moves = self.productionSystem(game)
        for move in moves:
            currGame = game.copy()
            currGame.applyMove(move)
            moveScores.put(Entry(move, self.minValue(currGame, self.searchDepth - 1, alpha, beta)))


        moves.clear()
        while not moveScores.empty():
            currEntry = moveScores.get()
            moves.append(currEntry.item)

        return None