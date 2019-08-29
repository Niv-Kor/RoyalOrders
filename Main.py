from MainWindow import MainWindow
from server.Protocol import Protocol
import Tkinter as tk


root = tk.Tk()
protocol = Protocol()
protocol.bind()
window = MainWindow(root, protocol)
root.mainloop()
