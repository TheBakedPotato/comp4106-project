import random

from player import Player
from move import Move

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
            if game.winner is not None:
                if game.winner == self:
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


        value = horizontalCounts[self.color]
        value += verticalCounts[self.color]
        value += upwardDiagonalCounts[self.color]
        value += downwardDiagonalCounts[self.color]
        value *= 5
        for player in game.players:
            if player != self:
                value -= horizontalCounts[player.color]
                value -= verticalCounts[player.color]
                value -= upwardDiagonalCounts[player.color]
                value -= downwardDiagonalCounts[player.color]

        return value

    
    def maxValue(self, game, move, player, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return Action(move, self.simpleHeuristic(game))

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
            return Action(move, self.simpleHeuristic(game))

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


    # def move(self, game, prevMove, prevGame):
    def move(self, game):
        alpha = float("-inf")
        beta = float("inf")

        action = self.maxValue(game, None, self, self.searchDepth, alpha, beta)
        return action.move


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