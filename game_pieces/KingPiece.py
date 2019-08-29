from Piece import Piece


class KingPiece(Piece):
    def __init__(self, board, color, size):
        Piece.__init__(self, board, 'king', color, size)

    def highlightPossibleMoves(self):
        # up
        self._scanGrid((self.gridXY[0], self.gridXY[1] - 1))

        # north-west
        self._scanGrid((self.gridXY[0] - 1, self.gridXY[1] - 1))

        # north-east
        self._scanGrid((self.gridXY[0] + 1, self.gridXY[1] - 1))

        # down
        self._scanGrid((self.gridXY[0], self.gridXY[1] + 1))

        # south-west
        self._scanGrid((self.gridXY[0] - 1, self.gridXY[1] + 1))

        # south-east
        self._scanGrid((self.gridXY[0] + 1, self.gridXY[1] + 1))

        # left
        self._scanGrid((self.gridXY[0] - 1, self.gridXY[1]))

        # right
        self._scanGrid((self.gridXY[0] + 1, self.gridXY[1]))
