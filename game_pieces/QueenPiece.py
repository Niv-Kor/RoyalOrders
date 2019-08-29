from Piece import Piece


class QueenPiece(Piece):
    def __init__(self, board, color, size):
        Piece.__init__(self, board, 'queen', color, size)

    def highlightPossibleMoves(self):
        # upwards
        scanRange = range(self.gridXY[1] - 1, -1, -1)
        self._scanVerticalMoves(scanRange)

        # downwards
        scanRange = range(self.gridXY[1] + 1, self.board.gridLine)
        self._scanVerticalMoves(scanRange)

        # left
        scanRange = range(self.gridXY[0] - 1, -1, -1)
        self._scanHorizontalMoves(scanRange)

        # right
        scanRange = range(self.gridXY[0] + 1, self.board.gridLine)
        self._scanHorizontalMoves(scanRange)

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
