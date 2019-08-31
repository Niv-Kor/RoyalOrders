from MainWindow import MainWindow
from server.Protocol import Protocol
import Tkinter as tk
from threading import Thread


def initLoop():
    root.mainloop()


root = tk.Tk()
protocol = Protocol()
protocol.bind()
window = MainWindow(root, protocol)

window.initThreads()
Thread(target=initLoop).start()

