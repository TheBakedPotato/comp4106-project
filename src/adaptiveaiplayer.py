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
        self.moveCount = 0


    def productionSystem(self, game, player=None):
        moves = []
        if player is None:
            player = self

        for column in range(game.board.xSize):
            if game.validColumn(column):
                moves.append(Move(player, column))

        return moves


    def simpleHeuristic(self, game, player):
        if game.gameOver:
            if game.winner is not None and game.winner == player:
                return float("inf")
            else:
                return float("-inf")

        lineSize = 4

        horizontalCounts = game.playerHorizontalOpenLinesCount(lineSize)
        verticalCounts = game.playerVerticalOpenLinesCount(lineSize)
        upwardDiagonalCounts = game.playerUpwardDiagonalOpenLinesCount(lineSize)
        downwardDiagonalCounts = game.playerDownwardDiagonalOpenLinesCount(lineSize)


        value = horizontalCounts[player.color]
        value += verticalCounts[player.color]
        value += upwardDiagonalCounts[player.color]
        value += downwardDiagonalCounts[player.color]
        for currPlayer in game.players:
            if currPlayer != player:
                value -= horizontalCounts[currPlayer.color]
                value -= verticalCounts[currPlayer.color]
                value -= upwardDiagonalCounts[currPlayer.color]
                value -= downwardDiagonalCounts[currPlayer.color]

        return value


    def maxValue(self, game, player, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return self.simpleHeuristic(game, player)

        value = float("-inf")
        moves = self.productionSystem(game, player)
        random.shuffle(moves)
        for currMove in moves:
            currGame = game.copy()
            currGame.applyMove(currMove)
            value = max(value, self.minValue(currGame, player, depth - 1, alpha, beta))
            if value >= beta:
                return value

            alpha = max(value, alpha)

        return value


    def minValue(self, game, player, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return self.simpleHeuristic(game, player)

        value = float("inf")
        for playerIndex in range(len(game.players)):
            if game.players[playerIndex] != player:
                moves = self.productionSystem(game, game.players[playerIndex])
                random.shuffle(moves)
                for currMove in moves:
                    currGame = game.copy()
                    currGame.applyMove(currMove)
                    value = min(value, self.maxValue(currGame, player, depth - 1, alpha, beta))
                    if value <= alpha:
                        return value

                    beta = min(value, beta)

        return value


    def moveOpponent(self, game, opponentMove):
        moveScores = PriorityQueue()

        alpha = float("-inf")
        beta = float("inf")

        moves = self.productionSystem(game, opponentMove.player)
        for move in moves:
            currGame = game.copy()
            currGame.applyMove(move)
            moveScores.put(Entry(move, self.minValue(currGame, opponentMove.player, self.searchDepth - 1, alpha, beta)))

        rank = 0
        while not moveScores.empty():
            rank += 1
            move = moveScores.get().item
            if move == opponentMove:
                break


        rankIncrease = rank
        if self.moveCount > 0:
            rankIncrease /= self.moveCount
            self.opponentRank += rankIncrease
        else:
            self.opponentRank = rank


    def move(self, game, prevMove, prevGame):
        move = None
        moveScores = PriorityQueue()

        alpha = float("-inf")
        beta = float("inf")

        if prevMove is not None:
            self.moveOpponent(prevGame, prevMove)
            self.moveCount += 1

        moves = self.productionSystem(game)
        for move in moves:
            currGame = game.copy()
            currGame.applyMove(move)
            moveScores.put(Entry(move, self.minValue(currGame, self, self.searchDepth - 1, alpha, beta)))

        moves.clear()
        while not moveScores.empty():
            currEntry = moveScores.get()
            moves.append(currEntry.item)

        rank = self.opponentRank
        if rank >= len(moves):
            rank = len(moves) - 1
        
        return moves[rank]