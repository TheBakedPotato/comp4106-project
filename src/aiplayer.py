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


    def simpleHeuristic(self, player, game, oldOpenLineValues):
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

    
    def maxValue(self):
        pass


    def minValue(self, game, oldOpenLineValues, depth, alpha, beta):
        if (depth == 0) or (game.gameOver):
            return self.simpleHeuristic()


    def move(self, game):
        move = None
        
        alpha = float("-inf")
        beta = float("inf")

        maxVal = float("-inf")
        oldOpenLineValues = game.checkPlayerOpenLines()
        for currMove in self.productionSystem(game):
            currGame = game.copy()
            print(currMove.player.color, currMove.column)
            currGame.applyMove(currMove)
            currVal = self.simpleHeuristic(self, currGame, oldOpenLineValues)
            # print("CurrMove: {}, CurrVal: {}".format(currMove, currVal))
            if currVal > maxVal:
                maxVal = currVal
                move = currMove

        # print("MaxVal: {}".format(maxVal))
        return move
