import tkinter as tk
import numpy as np
import random
from IO.PieceDragger import PieceDragger
from PIL import Image, ImageTk, ImageFile
from Grid import Grid
from game_pieces import PiecesFactory


BOARD_PERCENT = 0.9


class Board(tk.Canvas):
    def __init__(self, root, size):
        tk.Canvas.__init__(self, root, width=int(size * BOARD_PERCENT), height=size)
        self.gridLine = 8
        self.width, self.height = size, size
        self.gridSize = int(size * BOARD_PERCENT) / self.gridLine
        self._grids = np.array([[None] * self.gridLine] * self.gridLine)
        self._hightlightGrids = []
        self._dragger = PieceDragger(self)
        self.topY = int(size * (1 - BOARD_PERCENT))
        self._rotatedGridImages = {}
        self._setBoardGrids()

        # print logo on board
        self.logo = ImageTk.PhotoImage(Image.open('resources/logo.png'))
        self.create_image((self.width / 2 - 40, self.height / 2 + 15), image=self.logo)

        # arrange initial pieces
        self._setBoardPieces()

    def _setBoardGrids(self):
        # two images for grids - light and dark
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        lightImg = Image.open('resources/light_wood.png')
        lightImg = lightImg.resize((self.gridSize, self.gridSize), Image.ANTIALIAS)

        darkImg = Image.open('resources/dark_wood.png')
        darkImg = darkImg.resize((self.gridSize, self.gridSize), Image.ANTIALIAS)

        rotations = [0, 90, 180, 270]
        for r in rotations:
            self._rotatedGridImages[r] = [ImageTk.PhotoImage(lightImg.rotate(r)),
                                          ImageTk.PhotoImage(darkImg.rotate(r))]

        # set board grids
        for i in range(self.gridLine):
            for j in range(self.gridLine):
                offset = self.gridSize / 2
                pos = (i * self.gridSize + offset, self.topY + j * self.gridSize + offset)

                # even grid - light pattern
                if (i + j) % 2 == 0:
                    randomRotation = rotations[random.randint(0, len(rotations) - 1)]
                    lightImg = self._rotatedGridImages[randomRotation][0]
                    grid = Grid(self, self.gridSize, image=lightImg, XY=(i, j))
                # odd grid - dark pattern
                else:
                    randomRotation = rotations[random.randint(0, len(rotations) - 1)]
                    darkImg = self._rotatedGridImages[randomRotation][1]
                    grid = Grid(self, self.gridSize, image=darkImg, XY=(i, j))

                grid.show(pos)
                self._grids[i][j] = grid

    def _setBoardPieces(self):
        # init game pieces
        PiecesFactory.createAll(self, self.gridSize)

        # pick a random color for each player
        colors = ['white', 'black']
        random.shuffle(colors)
        playerColor = colors[0]
        oppColor = colors[1]

        # pawns
        for i in range(self.gridLine):
            gridXY = (i, 1)
            self.setPiece(PiecesFactory.retrieve('pawn', oppColor), gridXY, False, False)

        for i in range(self.gridLine):
            gridXY = (i, self.gridLine - 2)
            self.setPiece(PiecesFactory.retrieve('pawn', playerColor), gridXY, True, False)

        # rooks
        gridXY = (0, 0)
        self.setPiece(PiecesFactory.retrieve('rook', oppColor), gridXY, False, False)
        gridXY = (self.gridLine - 1, 0)
        self.setPiece(PiecesFactory.retrieve('rook', oppColor), gridXY, False, False)

        gridXY = (0, self.gridLine - 1)
        self.setPiece(PiecesFactory.retrieve('rook', playerColor), gridXY, True, False)
        gridXY = (self.gridLine - 1, self.gridLine - 1)
        self.setPiece(PiecesFactory.retrieve('rook', playerColor), gridXY, True, False)

        # knights
        gridXY = (1, 0)
        self.setPiece(PiecesFactory.retrieve('knight', oppColor), gridXY, False, False)
        gridXY = (self.gridLine - 2, 0)
        self.setPiece(PiecesFactory.retrieve('knight', oppColor), gridXY, False, False)

        gridXY = (1, self.gridLine - 1)
        self.setPiece(PiecesFactory.retrieve('knight', playerColor), gridXY, True, False)
        gridXY = (self.gridLine - 2, self.gridLine - 1)
        self.setPiece(PiecesFactory.retrieve('knight', playerColor), gridXY, True, False)

        # bishops
        gridXY = (2, 0)
        self.setPiece(PiecesFactory.retrieve('bishop', oppColor), gridXY, False, False)
        gridXY = (self.gridLine - 3, 0)
        self.setPiece(PiecesFactory.retrieve('bishop', oppColor), gridXY, False, False)

        gridXY = (2, self.gridLine - 1)
        self.setPiece(PiecesFactory.retrieve('bishop', playerColor), gridXY, True, False)
        gridXY = (self.gridLine - 3, self.gridLine - 1)
        self.setPiece(PiecesFactory.retrieve('bishop', playerColor), gridXY, True, False)

        # queens
        gridXY = (4, 0)
        self.setPiece(PiecesFactory.retrieve('queen', oppColor), gridXY, False, False)
        gridXY = (4, self.gridLine - 1)
        self.setPiece(PiecesFactory.retrieve('queen', playerColor), gridXY, True, False)

        # kings
        gridXY = (3, 0)
        self.setPiece(PiecesFactory.retrieve('king', oppColor), gridXY, False, False)
        gridXY = (3, self.gridLine - 1)
        self.setPiece(PiecesFactory.retrieve('king', playerColor), gridXY, True, False)

    def setPiece(self, piece, (x, y), playable, diffGrid, pos=None):
        self._grids[x][y].occupy(piece, pos, playable, diffGrid)

    def highlightGrid(self, (x, y)):
        if x not in range(self.gridLine) or y not in range(self.gridLine):
            return

        if self._grids[x][y].isOccupied():
            return

        grid = self._grids[x][y]
        grid.highlight(True)
        self._hightlightGrids.append(grid)

    def targetGrid(self, (x, y)):
        if x not in range(self.gridLine) or y not in range(self.gridLine):
            return

        if not self._grids[x][y].isOccupied():
            return

        grid = self._grids[x][y]
        grid.target(True)
        self._hightlightGrids.append(grid)

    def isHighlighted(self, grid):
        for g in self._hightlightGrids:
            if g.gridXY == grid:
                return True
        else:
            return False

    def cancelHighlights(self):
        for g in self._hightlightGrids:
            g.highlight(False)
            g.target(False)

        self._hightlightGrids = []

    # Find a grid that fully contains the argument rect
    def findGrid(self, (A, B, C)):
        suspectA = (A[0] / self.gridSize, A[1] / self.gridSize)
        suspectB = (B[0] / self.gridSize, B[1] / self.gridSize)
        minGridY = self.getGrid(suspectA).position[1] + self.gridSize / 2

        if suspectB == suspectA and C[1] < minGridY:
            return suspectA
        else:
            return None

    def getGrid(self, (x, y)):
        try:
            return self._grids[x][y]
        except IndexError:
            return None
