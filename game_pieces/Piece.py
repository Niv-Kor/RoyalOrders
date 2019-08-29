from PIL import Image, ImageTk
import abc


class Piece:
    def __init__(self, board, pieceName, color, size):
        self.name = color + '_' + pieceName
        size = int(size * 0.5)
        img = Image.open('resources/pieces/' + self.name + '.png').convert("RGBA")
        oldSize = img.size

        widthPerc = (size / float(oldSize[0]))
        newHeight = int((float(oldSize[1]) * float(widthPerc)))

        img = img.resize((size, newHeight), Image.ANTIALIAS)
        self.imgSize = img.size
        self.image = ImageTk.PhotoImage(img)
        self.board = board
        self.gridXY = (-1, -1)
        self._position = None
        self._moveCounter = 0
        self._playable = False

    def move(self, pos, XY, diffGrid):
        self.gridXY = XY
        self._position = pos

        if diffGrid:
            self._moveCounter += 1

    # Change the playability status of this piece.
    # Playable pieces belong to the player.
    def setPlayability(self, flag):
        self._playable = flag

    # Check if this piece belongs to the player or rather to the opponent.
    def isFriendly(self):
        return self._playable

    # Get the minimal area of the piece that the grid should contain.
    def getAnchor(self):
        anchor = (self._position[0], self._position[1] - self.board.topY)
        width, height = self.imgSize
        A = (anchor[0] - width / 4, anchor[1] + height / 4)
        B = (anchor[0] + width / 4, anchor[1] + height / 4)
        C = (anchor[0], anchor[1] + height / 2)
        return A, B, C

    def _scanGrid(self, grid):
        self.board.highlightGrid(grid)
        gridObj = self.board.getGrid(grid)

        if gridObj is not None and gridObj.isOccupied():
            self._tryTarget(grid)
            return False  # encountered blockage

        return True

    def _scanVerticalMoves(self, yRange):
        for i in yRange:
            if not self._scanGrid((self.gridXY[0], i)):
                break

    def _scanHorizontalMoves(self, xRange):
        for i in xRange:
            if not self._scanGrid((i, self.gridXY[1])):
                break

    def _scanDiagonalMoves(self, xRange, yRange):
        for i, j in zip(xRange, yRange):
            if not self._scanGrid((i, j)):
                break

    def _tryTarget(self, grid):
        gridObj = self.board.getGrid(grid)

        if gridObj is not None:
            targetPiece = gridObj.getOccupation()
            if targetPiece is not None and not targetPiece.isFriendly():
                self.board.targetGrid(grid)

    @abc.abstractmethod
    def highlightPossibleMoves(self):
        pass
