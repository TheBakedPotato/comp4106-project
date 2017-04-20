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
            if game.winner is not None:
                if game.winner == player:
                    return float("inf")
                else:
                    return float("-inf")
            else:
                return 0

        lineSize = 4

        horizontalCounts = game.playerHorizontalOpenLinesCount(lineSize)
        verticalCounts = game.playerVerticalOpenLinesCount(lineSize)
        upwardDiagonalCounts = game.playerUpwardDiagonalOpenLinesCount(lineSize)
        downwardDiagonalCounts = game.playerDownwardDiagonalOpenLinesCount(lineSize)


        value = horizontalCounts[player.color]
        value += verticalCounts[player.color]
        value += upwardDiagonalCounts[player.color]
        value += downwardDiagonalCounts[player.color]
        value *= 5
        for currPlayer in game.players:
            if currPlayer != player:
                value -= horizontalCounts[currPlayer.color]
                value -= verticalCounts[currPlayer.color]
                value -= upwardDiagonalCounts[currPlayer.color]
                value -= downwardDiagonalCounts[currPlayer.color]

        return value


    def maxValue(self, game, move, player, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return Action(move, self.simpleHeuristic(game, player))

        action = None
        moves = self.productionSystem(game, player)
        random.shuffle(moves)
        for currMove in moves:
            currGame = game.copy()
            currGame.applyMove(currMove)
            currAction = self.minValue(currGame, currMove, player, depth - 1, alpha, beta)

            if (action is None) or (currAction.value > action.value):
                action = Action(currMove, currAction.value)

            if (action is not None) and (action.value >= beta):
                return action

            if (action is not None) and (action.value > alpha):
                alpha = action.value

        return action


    def minValue(self, game, move, player, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return Action(move, self.simpleHeuristic(game, player))

        action = None
        for playerIndex in range(len(game.players)):
            if game.players[playerIndex] != player:
                currPlayer = game.players[playerIndex]
                moves = self.productionSystem(game, currPlayer)
                random.shuffle(moves)
                for currMove in moves:
                    currGame = game.copy()
                    currGame.applyMove(currMove)
                    currAction = self.maxValue(currGame, currMove, player, depth - 1, alpha, beta)

                    if (action is None) or (currAction.value < action.value):
                        action = Action(currMove, currAction.value)

                    if (action is not None) and (action.value <= alpha):
                        return action

                    if (action is not None) and (action.value < beta):
                        beta = action.value

        return action


    # def moveOpponent(self, game, opponentMove):
    #     self.moveCount += 1
    #     moveScores = PriorityQueue()

    #     alpha = float("-inf")
    #     beta = float("inf")

    #     print("Opponent Move: {}")
    #     moves = self.productionSystem(game, opponentMove.player)
    #     # random.shuffle(moves)
    #     for move in moves:
    #         currGame = game.copy()
    #         currGame.applyMove(move)
    #         score = self.minValue(currGame, opponentMove.player, self.searchDepth - 1, alpha, beta)
    #         moveScores.put(Entry(move, score))
    #         print("Move: {}, Score: {}".format(move.column, score))

    #     self.opponentRank = 1


    # def move(self, game, prevMove, prevGame):
    # def move(self, game):
    #     alpha = float("-inf")
    #     beta = float("inf")

    #     action = self.maxValue(game, None, self, self.searchDepth, alpha, beta)
    #     return action.move


    def move(self, game):
        alpha = float("-inf")
        beta = float("inf")

        playerActions = []
        moves = self.productionSystem(game, self)
        random.shuffle(moves)
        for move in moves:
            currGame = game.copy()
            currGame.applyMove(move)
            action = Action(move, self.minValue(currGame, move, self, self.searchDepth - 1, alpha, beta).value)
            playerActions.append(action)
        playerActions = sorted(playerActions)
        return playerActions[len(playerActions) - 1].move


class Action:

    def __init__(self, move, value):
        self.move = move
        self.value = value


    def __eq__(self, other):
        return self.value == other.value


    def __ne__(self, other):
        return not (self.value == other.value)


    def __lt__(self, other):
        return self.value < other.value


    def __gt__(self, other):
        return self.value > other.value


    def __le__(self, other):
        return (self < other) or (self == other)


    def __ge__(self, other):
        return (self > other) or (self == other)

        # maxScore = 0
        # moveScore = float("inf")
        # moveRank = 0
        # rank = 1
        # scoreCount = 0
        # while not moveScores.empty():
        #     entry = moveScores.get()
        #     # maxScore = entry.value
        #     if entry.item == opponentMove:
        #         # moveValue = entry.value
        #         moveScore = entry.value
        #         moveRank = rank
        #     elif entry.value == moveScore:
        #         scoreCount += 1
        #     elif entry.value > moveScore:
        #         break
        #     rank += 1

        # moveRank = (scoreCount / 2) + moveRank

        # if len(moves) > 1:
        #     rank = rank / len(moves)
        #     self.opponentRank = (self.opponentRank * (self.moveCount - 1) + rank) / self.moveCount
        # print(self.opponentRank)

        # if len(moves) > 1:
        #     moveRank = moveRank / len(moves)
        #     self.opponentRank = (self.opponentRank * (self.moveCount - 1) + moveRank) / self.moveCount
        # print(self.opponentRank)

        # print(self.opponentRank)
        # print("Move Value: {}, Max Score: {}".format(moveValue, maxScore))
        # if maxScore == float("inf") or moveValue == float("inf"):
        #     rank = 1
        # elif moveValue == float("-inf") or maxScore == float("-inf") or maxScore == 0:
        #     rank = 0
        # else:
        #     rank = moveValue / maxScore
        # print("Rank: {}".format(rank))
        # self.opponentRank = (self.opponentRank * (self.moveCount - 1) + rank) / self.moveCount
        # print(self.opponentRank)