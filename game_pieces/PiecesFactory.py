from game_pieces.PawnPiece import PawnPiece
from game_pieces.RookPiece import RookPiece
from game_pieces.KnightPiece import KnightPiece
from game_pieces.BishopPiece import BishopPiece
from game_pieces.QueenPiece import QueenPiece
from game_pieces.KingPiece import KingPiece


_pieceByID = {}
_IDByPiece = {}
_pieces = {'pawn': {'white': [], 'black': []},
           'rook': {'white': [], 'black': []},
           'knight': {'white': [], 'black': []},
           'bishop': {'white': [], 'black': []},
           'queen': {'white': [], 'black': []},
           'king': {'white': [], 'black': []}}


def createAll(board, gridSize):
    create('pawn', 'black', board, gridSize, 8)
    create('pawn', 'white', board, gridSize, 8)
    create('rook', 'black', board, gridSize, 2)
    create('rook', 'white', board, gridSize, 2)
    create('knight', 'black', board, gridSize, 2)
    create('knight', 'white', board, gridSize, 2)
    create('bishop', 'black', board, gridSize, 2)
    create('bishop', 'white', board, gridSize, 2)
    create('queen', 'black', board, gridSize, 1)
    create('queen', 'white', board, gridSize, 1)
    create('king', 'black', board, gridSize, 1)
    create('king', 'white', board, gridSize, 1)


def create(name, color, board, gridSize, amount):
    if amount <= 0:
        return
    else:
        if name == 'pawn':
            piece = PawnPiece(board, color, gridSize)
        elif name == 'rook':
            piece = RookPiece(board, color, gridSize)
        elif name == 'knight':
            piece = KnightPiece(board, color, gridSize)
        elif name == 'bishop':
            piece = BishopPiece(board, color, gridSize)
        elif name == 'queen':
            piece = QueenPiece(board, color, gridSize)
        elif name == 'king':
            piece = KingPiece(board, color, gridSize)
        else:
            return None

        _pieces[name][color].append(piece)
        create(name, color, board, gridSize, amount - 1)


def retrieve(name, color):
    return _pieces[name][color].pop()


def appendID(itemID, piece):
    _pieceByID[itemID] = piece
    _IDByPiece[piece] = itemID


def removeID(itemID=None, piece=None):
    if itemID is not None:
        value = _pieceByID[itemID]
        del _pieceByID[itemID]
        del _IDByPiece[value]
    elif piece is not None:
        value = _IDByPiece[piece]
        del _IDByPiece[piece]
        del _pieceByID[value]


def identifyByID(itemID):
    return _pieceByID.get(itemID)


def identifyByObj(piece):
    return _IDByPiece.get(piece)


def clearIDs():
    _pieceByID.clear()
    _IDByPiece.clear()
