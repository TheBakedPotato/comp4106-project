from player import Player
from move import Move
from position import Position

class AIPlayer(Player):

    def __init__(self, color, heuristic, searchDepth):
        super().__init__(color)
        self.heuristic = heuristic
        self.searchDepth = searchDepth


    def productionSystem(self, game):
        moves = []

        for column in range(game.board.xSize):
            if game.validColumn(column):
                moves.append(column)

        return moves


    def move(self, game):
        move = None
        moves = self.productionSystem(game)
        if len(moves) > 0:
            move = moves[0]

        return move

    # def productionSystem(self, board):
    #     moves = []
    #     jumpPossible = False

    #     for tilePos, gamePiece in board.board.items():
    #         if gamePiece.color == self.color:
    #             pieceMoves, jumpMoves = self.makeMoves(board, tilePos)
    #             if jumpMoves:
    #                 if not jumpPossible:
    #                     jumpPossible = True
    #                     moves.clear()
    #                 moves += pieceMoves
    #             elif not jumpPossible:
    #                 moves += pieceMoves

    #     return moves


    # def makeMoves(self, board, pos):
    #     moves = []
    #     jumpPossible = False

    #     gamePiece = board.board[pos]
    #     for direction in gamePiece.directions:
    #         newY = pos.y + direction
    #         for dX in range(-1, 2):
    #             newPos = Position(pos.x + dX, newY)
    #             if (newPos.x != pos.x) and board.validPosition(newPos):
    #                 if newPos in board.board:
    #                     newPos = self.jumpPosition(board, pos, newPos)
    #                     if newPos is not None:
    #                         if not jumpPossible:
    #                             jumpPossible = True
    #                             moves.clear()

    #                         moves.append(Move(pos, newPos))

    #                 elif not jumpPossible:
    #                     moves.append(Move(pos, newPos))

    #     return (moves, jumpPossible)


    # def jumpPosition(self, board, startPos, jumpPos):
    #     startPiece = board.board[startPos]
    #     jumpPiece = board.board[jumpPos]

    #     if startPiece.color == jumpPiece.color:
    #         return None

    #     dX = jumpPos.x - startPos.x
    #     dY = jumpPos.y - startPos.y

    #     newPos = Position(startPos.x + (2 * dX), startPos.y + (2 * dY))
    #     if newPos in board.board or not board.validPosition(newPos):
    #         return None

    #     return newPos


    # def move(self, board):
    #     moves = self.productionSystem(board)

    #     return moves[0]