from server import ServerConstants as servconst
from PIL import ImageTk, Image
import Tkinter as tk
from server import Protocol
from board import Board
from threading import Thread
from GameController import GameController


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 850
BOARD_AREA = int(WINDOW_HEIGHT * 0.9)
BOARD_POSITION = (20, WINDOW_HEIGHT - BOARD_AREA - 20)


class MainWindow:
    def __init__(self, root, protocol):
        self.protocol = protocol
        self.waiting = False

        # window configuration
        self.root = root
        self.root.title(servconst.APP_NAME)
        self.root.resizable(False, False)

        xPos = self.root.winfo_screenwidth() / 2 - WINDOW_WIDTH / 2
        yPos = self.root.winfo_screenheight() / 2 - WINDOW_HEIGHT / 2
        self.root.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, xPos, yPos))

        # precreation of the board
        self.board = Board.Board(self.root, BOARD_AREA)

        # enter button
        self.enterButton = tk.Button(self.root, command=self.__waitForOpponent)
        self.enterButton.grid(pady=(300, 0), padx=(WINDOW_WIDTH / 2, 0))

        regImg = ImageTk.PhotoImage(Image.open('resources/play_button.png'))
        hoverImg = ImageTk.PhotoImage(Image.open('resources/play_button_hover.png'))
        self.enterButton.config(image=regImg, highlightthickness=0, bd=0)

        self.enterButton.bind("<Enter>", lambda event, h=self.enterButton: h.configure(image=hoverImg))
        self.enterButton.bind("<Leave>", lambda event, h=self.enterButton: h.configure(image=regImg))

        # wait for opponent in separate thread
        Thread(target=self.__playOnline).start()

    def __waitForOpponent(self):
        self.waiting = True

    def __playOnline(self):
        while True:
            if self.waiting:
                break

        message = {'type': servconst.GAME_SEARCH_MESSAGE}
        self.protocol.send(message)

        # wait for response from server
        try:
            while True:
                print 'wait'

                msg = self.protocol.receive()
                msg = Protocol.toDictionary(msg)
                print 'got', msg

                if msg['type'] == servconst.GAME_SEARCH_MESSAGE:
                    if msg['permit'] is -1:  # forbid
                        print '>>> Could not find an opponent. Please try again later.'
                    elif msg['permit'] is 0:  # wait
                        print '>>> Waiting for an opponent.'
                        continue
                    else:  # allow
                        self.enterButton.grid_remove()
                        self.board.place(x=BOARD_POSITION[0], y=BOARD_POSITION[1])
                        controller = GameController()
                        controller.connect(self.protocol, self.board)

                    break  # permit is either -1 or 1
        except Exception:
            pass
