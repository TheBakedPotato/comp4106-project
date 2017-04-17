from player import Player
from move import Move
from position import Position

class AIPlayer(Player):

    def __init__(self, color, searchDepth):
        super().__init__(color)
        self.searchDepth = searchDepth


    def productionSystem(self, game):
        moves = []

        for column in range(game.board.xSize):
            if game.validColumn(column):
                moves.append(column)

        return moves


    def simpleHeuristic(self, player, game, oldOpenLineValues):
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


    def move(self, game):
        move = None
        moves = self.productionSystem(game)
        maxVal = float("-inf")
        oldOpenLineValues = game.checkPlayerOpenLines()
        for currMove in moves:
            currGame = game.copy()
            currGame.applyMove(self, currMove)
            currVal = self.simpleHeuristic(self, currGame, oldOpenLineValues)
            print("CurrMove: {}, CurrVal: {}".format(currMove, currVal))
            if currVal > maxVal:
                maxVal = currVal
                move = currMove

        print("MaxVal: {}".format(maxVal))
        return move
