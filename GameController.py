from threading import Thread
from server import ServerConstants as servconst
import ast


class GameController:
    def __init__(self, board):
        self.board = board
        self.protocol = None
        self.window = None
        self.partner = None

    def connect(self, protocol, window):
        self.protocol = protocol
        self.window = window
        self.window.connectController(self)
        receiveThread = Thread(target=self.receive)
        receiveThread.start()

    # receive a message from either the server or the other client
    def receive(self):
        while True:
            msg = ast.literal_eval(self.protocol.receive())
            print 'received', msg

            if not type(msg) is None:
                if msg['type'] == servconst.GAME_MOVE:
                    prevGrid = msg['prev_grid']
                    nextGrid = msg['next_grid']
                    self.board.forceMove(prevGrid, nextGrid)
            else:  # client has possibly left the game
                break

    # Send a message to the other client
    def send(self, msg):
        # close the window
        if msg == servconst.QUIT_MESSAGE:
            self.window.close()
        # client sends a legal message
        else:
            self.protocol.send(msg)

    def close(self):
        self.send(servconst.QUIT_MESSAGE)
