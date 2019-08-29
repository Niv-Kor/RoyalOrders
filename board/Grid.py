from PIL import Image, ImageTk
from game_pieces import PiecesFactory


class Grid:
    def __init__(self, board, size, image, XY):
        self.board = board
        self.image = image
        self._occupation = None
        self.size = size
        self.position = 0
        self.gridXY = XY

        # grid highlight image
        rawMarkerImg = Image.open('resources/highlight.png')
        rawMarkerImg = rawMarkerImg.resize((self.size, self.size), Image.ANTIALIAS)
        self._highlightImg = ImageTk.PhotoImage(rawMarkerImg)
        self._highlightItem = None  # the actual canvas image

        # grid target image (for occupying a prey opponent piece)
        rawTargetImg = Image.open('resources/target.png')
        rawTargetImg = rawTargetImg.resize((self.size, self.size), Image.ANTIALIAS)
        self._targetImg = ImageTk.PhotoImage(rawTargetImg)
        self._targetItem = None  # the actual canvas image

    def show(self, pos):
        self.board.create_image(pos, image=self.image)
        self.position = pos

    def highlight(self, flag):
        if flag:
            self._highlightItem = self.board.create_image(self.position, image=self._highlightImg)
        else:
            self.board.delete(self._highlightItem)

    def target(self, flag):
        if flag:
            self._targetItem = self.board.create_image(self.position, image=self._targetImg)
        else:
            self.board.delete(self._targetItem)

    def isOccupied(self):
        return self._occupation is not None

    def occupy(self, piece, pos, playable, diffGrid):
        self.free()
        self._occupation = piece

        if piece is not None:
            tagSwitch = {True: 'playable', False: 'non-playable'}

            # position is determined
            if pos is None:
                position = (self.position[0], self.position[1] - self.size / 4)
            # default 3D position
            else:
                position = pos

            piece.setPlayability(playable)
            piece.move(position, self.gridXY, diffGrid)
            itemID = self.board.create_image(position, image=piece.image,
                                             tags=tagSwitch.get(playable))

            # identify the piece object with its item id for later use
            PiecesFactory.appendID(itemID, piece)

    def free(self):
        if self.isOccupied():
            itemID = PiecesFactory.identifyByObj(self._occupation)
            PiecesFactory.removeID(piece=self._occupation)
            self.board.delete(itemID)

        self._occupation = None

    # Get the piece that occopies this grid
    def getOccupation(self):
        return self._occupation
