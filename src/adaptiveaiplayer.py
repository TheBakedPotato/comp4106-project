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
        self.opponentRank = 0
        self.moveCount = 0


    def productionSystem(self, game, player=None):
        moves = []
        if player is None:
            player = self

        for column in range(game.board.xSize):
            if game.validColumn(column):
                moves.append(Move(player, column))

        return moves


    def simpleHeuristic(self, game, player, depth):
        if game.gameOver:
            if game.winner is not None:
                value = self.maxHeuristicValue - (self.searchDepth - depth)
                if game.winner == player:
                    return value
                else:
                    return (value * -1)
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
            return Action(move, self.simpleHeuristic(game, player, depth))

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
            return Action(move, self.simpleHeuristic(game, player, depth))

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


    def moveOpponent(self, game, opponentMove):
        self.moveCount += 1
        opponent = opponentMove.player

        alpha = float("-inf")
        beta = float("inf")
        moves = self.productionSystem(game, opponent)
        opponentActions = []
        for move in moves:
            currGame = game.copy()
            currGame.applyMove(move)
            action = Action(move, self.minValue(currGame, move, opponent, self.searchDepth - 1, alpha, beta).value)
            opponentActions.append(action)
        opponentActions = sorted(opponentActions)

        movePos = 0
        if len(opponentActions) > 1:
            for pos in range(len(opponentActions)):
                if opponentActions[pos].move == opponentMove:
                    break
                movePos += 1
            
            movePos = movePos / (len(opponentActions) - 1)
        else:
            movePos = 0.5

        self.opponentRank = (self.opponentRank * (self.moveCount - 1) + movePos) / self.moveCount

    
    def move(self, game, prevMove, prevGame):
        alpha = float("-inf")
        beta = float("inf")

        if prevMove is not None:
            self.moveOpponent(prevGame, prevMove)

        playerActions = []
        moves = self.productionSystem(game, self)
        random.shuffle(moves)
        for move in moves:
            currGame = game.copy()
            currGame.applyMove(move)
            action = Action(move, self.minValue(currGame, move, self, self.searchDepth - 1, alpha, beta).value)
            playerActions.append(action)
        playerActions = sorted(playerActions)

        if len(playerActions) > 1:
            return playerActions[round(self.opponentRank * (len(playerActions) - 1))].move
        else:
            return playerActions[0].move


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