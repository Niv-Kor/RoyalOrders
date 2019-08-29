from Piece import Piece


class BishopPiece(Piece):
    def __init__(self, board, color, size):
        Piece.__init__(self, board, 'bishop', color, size)

    def highlightPossibleMoves(self):
        # north-west
        xRange = range(self.gridXY[0] - 1, -1, -1)
        yRange = range(self.gridXY[1] - 1, -1, -1)
        self._scanDiagonalMoves(xRange, yRange)

        # north-east
        xRange = range(self.gridXY[0] + 1, self.board.gridLine)
        yRange = range(self.gridXY[1] - 1, -1, -1)
        self._scanDiagonalMoves(xRange, yRange)

        # south-west
        xRange = range(self.gridXY[0] - 1, -1, -1)
        yRange = range(self.gridXY[1] + 1, self.board.gridLine)
        self._scanDiagonalMoves(xRange, yRange)

        # south-east
        xRange = range(self.gridXY[0] + 1, self.board.gridLine)
        yRange = range(self.gridXY[1] + 1, self.board.gridLine)
        self._scanDiagonalMoves(xRange, yRange)
