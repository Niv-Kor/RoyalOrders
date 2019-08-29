from Piece import Piece


class PawnPiece(Piece):
    def __init__(self, board, color, size):
        Piece.__init__(self, board, 'pawn', color, size)

    def highlightPossibleMoves(self):
        regGrid = (self.gridXY[0], self.gridXY[1] - 1)
        self.board.highlightGrid(regGrid)

        # first movement
        if self._moveCounter < 1:
            bonusStartGrid = (self.gridXY[0], self.gridXY[1] - 2)
            self.board.highlightGrid(bonusStartGrid)

        # targets
        self._tryTarget((self.gridXY[0] - 1, self.gridXY[1] - 1))
        self._tryTarget((self.gridXY[0] + 1, self.gridXY[1] - 1))
