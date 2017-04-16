from position import Position
from gamepiece import GamePiece
from move import Move

class CheckersBoard:
    
    def __init__(self, size, colors):
        self.board = {}
        self.size = size
        # self.createBoard(colors)
        self.createTestBoard(colors)


    def createBoard(self, colors):
        blackYLimit = (self.size / 2) - 1
        whiteYLimit = (self.size / 2) + 1
        currCount = 0
        for y in range(self.size):
            for x in range(self.size):
                if ((x - y) % 2 == 1):
                    pos = Position(x,y)
                    if y < blackYLimit:
                        self.board[pos] = GamePiece(colors[0], {1})
                    elif y >= whiteYLimit:
                        self.board[pos] = GamePiece(colors[1], {-1})


    def createTestBoard(self, colors):
        blackYLimit = (self.size / 2)
        whiteYLimit = (self.size / 2) + 1
        currCount = 0
        for y in range(self.size):
            for x in range(self.size):
                if ((x - y) % 2 == 1):
                    pos = Position(x,y)
                    if (y != 0) and (y <= blackYLimit) and (y % 2 == 0):
                        self.board[pos] = GamePiece(colors[0], {1})
                    elif y >= whiteYLimit:
                        self.board[pos] = GamePiece(colors[1], {-1})


    def validXorY(self, xOrY):
        return (xOrY < self.size) and (xOrY >= 0)


    def validPosition(self, pos):
        return self.validXorY(pos.x) and self.validXorY(pos.y)


    def validPlayerPos(self, player, pos):
        if pos in self.board:
            return self.board[pos].color == player.color
        
        return False


    def getJumpPos(self, startPos, jumpPos):
        if self.board[startPos].color == self.board[jumpPos].color:
            return None

        dX = jumpPos.x - startPos.x
        dY = jumpPos.y - startPos.y

        endPos = Position(startPos.x + (2 * dX), startPos.y + (2 * dY))
        if (not self.validPosition(endPos)) or (endPos in self.board):
            return None

        return endPos


    def pieceMoves(self, pos):
        jumpMove = False
        moves = set()

        if pos not in self.board:
            return (moves, jumpMove)

        gamePiece = self.board[pos]
        for direction in gamePiece.directions:
            newY = pos.y + direction
            for dX in range(-1, 2):
                newPos = Position(pos.x + dX, newY)
                if (newPos.x != pos.x) and self.validPosition(newPos):
                    if (newPos not in self.board) and (not jumpMove):
                        moves.add(Move(pos, newPos))
                    elif self.board[newPos].color != gamePiece.color:
                        newPos = self.getJumpPos(pos, newPos)
                        if newPos:
                            if not jumpMove:
                                jumpMove = True
                                moves.clear()
                            moves.add(Move(pos, newPos))

        return (moves, jumpMove)


    def playerMoves(self, player):
        moves = set()
        hasJumpMove = False

        for tilePos, gamePiece in self.board.items():
            if gamePiece.color == player.color:
                pieceMoves, jumpAvailable = self.pieceMoves(tilePos)
                if jumpAvailable and hasJumpMove:
                    moves |= pieceMoves
                elif jumpAvailable:
                    hasJumpMove = True
                    moves.clear()
                    moves |= pieceMoves
                else:
                    moves |= pieceMoves

        return moves