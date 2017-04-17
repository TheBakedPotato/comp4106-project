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


    def simpleHeuristic(self, player, game):
        weightPlayerOpenLines = 1
        weightPlayerForks = 1
        weightOppoentClosedOpenLines = 1
        weightOpponentForks = 1



        return 0


    def move(self, game):
        move = None
        moves = self.productionSystem(game)
        if len(moves) > 0:
            move = moves[0]

        return move
