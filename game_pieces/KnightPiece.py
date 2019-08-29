from Piece import Piece


class KnightPiece(Piece):
    def __init__(self, board, color, size):
        Piece.__init__(self, board, 'knight', color, size)

    def highlightPossibleMoves(self):
        # north-west
        self._scanGrid((self.gridXY[0] - 1, self.gridXY[1] - 2))
        self._scanGrid((self.gridXY[0] - 2, self.gridXY[1] - 1))

        # north-east
        self._scanGrid((self.gridXY[0] + 1, self.gridXY[1] - 2))
        self._scanGrid((self.gridXY[0] + 2, self.gridXY[1] - 1))

        # south-west
        self._scanGrid((self.gridXY[0] - 1, self.gridXY[1] + 2))
        self._scanGrid((self.gridXY[0] - 2, self.gridXY[1] + 1))

        # south-east
        self._scanGrid((self.gridXY[0] + 1, self.gridXY[1] + 2))
        self._scanGrid((self.gridXY[0] + 2, self.gridXY[1] + 1))