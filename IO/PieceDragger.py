from game_pieces import PiecesFactory


class PieceDragger:
    def __init__(self, board):
        self.board = board

        # this data is used to keep track of an  item being dragged
        self._dragData = {'src_x': 0, 'src_y': 0, 'x': 0, 'y': 0,
                          'sourceAnchor': None, 'itemID': None, 'itemOBJ': None}

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.board.tag_bind('playable', '<ButtonPress-1>', self.onStart)
        self.board.tag_bind('playable', '<B1-Motion>', self.onDrag)
        self.board.tag_bind('playable', '<ButtonRelease-1>', self.onRelease)

    def onStart(self, event):
        # check that the received item ID is indeed the ID of a game piece.
        # this fixes a bug where sometimes the board grids get caught and dragged as well.
        itemID = self.board.find_closest(event.x, event.y)[0]
        if PiecesFactory.identifyByID(itemID) is None:
            return

        self._dragData['itemID'] = itemID
        self._dragData['itemOBJ'] = PiecesFactory.identifyByID(self._dragData['itemID'])
        self._dragData['sourceAnchor'] = self._dragData['itemOBJ'].getAnchor()
        self._dragData['src_x'] = event.x
        self._dragData['src_y'] = event.y
        self._dragData['x'] = event.x
        self._dragData['y'] = event.y

        # highlight the possible moves
        self._dragData['itemOBJ'].highlightPossibleMoves()

        # keep the playable pieces always on top
        self.board.tag_raise('playable')

    def onDrag(self, event):
        deltaX = event.x - self._dragData['x']
        deltaY = event.y - self._dragData['y']

        # move the object the appropriate amount
        self.board.move(self._dragData['itemID'], deltaX, deltaY)

        # record the new position
        self._dragData['x'] = event.x
        self._dragData['y'] = event.y

    def onRelease(self, event):
        # formally move the piece to a different grid if needed
        piece = self._dragData['itemOBJ']
        oldAnchor = self._dragData['sourceAnchor']
        deltaX = self._dragData['x'] - self._dragData['src_x']
        deltaY = self._dragData['y'] - self._dragData['src_y']
        newA = (oldAnchor[0][0] + deltaX, oldAnchor[0][1] + deltaY)
        newB = (oldAnchor[1][0] + deltaX, oldAnchor[1][1] + deltaY)
        newC = (oldAnchor[2][0] + deltaX, oldAnchor[2][1] + deltaY)
        newGrid = self.board.findGrid((newA, newB, newC))

        # player made a legal move to a new grid
        if newGrid is not None and (self.board.isHighlighted(newGrid) or newGrid == piece.gridXY):
            # don't increase move count because the piece didn't actually change its grids
            differentGrid = False if newGrid == piece.gridXY else True

            # free old grid
            oldGrid = self.board.getGrid(piece.gridXY)
            oldGrid.free()

            # set on new grid
            newPos = ((newA[0] + newB[0]) / 2, newA[1] - piece.imgSize[1] / 4 + self.board.topY)
            self.board.setPiece(piece, newGrid, True, differentGrid, newPos)

        # illegal move - back to the last stable spot
        else:
            oldPos = ((oldAnchor[0][0] + oldAnchor[1][0]) / 2,
                      oldAnchor[0][1] - piece.imgSize[1] / 4 + self.board.topY)

            self.board.setPiece(piece, piece.gridXY, True, False, oldPos)

        # turn of all highlights on the board
        self.board.cancelHighlights()

        self._dragData['itemID'] = None
        self._dragData['itemOBJ'] = None
        self._dragData['sourceAnchor'] = None
        self._dragData['src_x'] = 0
        self._dragData['src_y'] = 0
        self._dragData['x'] = 0
        self._dragData['y'] = 0
