import os
os.environ['TCL_LIBRARY'] = 'C:/Users/caiof/AppData/Local/Programs/Python/Python313/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'C:/Users/caiof/AppData/Local/Programs/Python/Python313/tcl/tk8.6'

import socket
import threading
import tkinter
from tkinter import *
from tkinter import simpledialog


class Chat:
    def __init__(self):

        HOST = '127.0.0.1'
        PORT = 55555

        #self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client.connect((HOST, PORT))

        login = Tk()
        login.withdraw()

        self.loaded_window = False
        self.active = True

        self.name = simpledialog.askstring('Name', 'Type your name', parent=login)

        self.room = simpledialog.askstring('Room', 'What room do you want to access?', parent=login)

        self.window()

    def window(self):
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title('Chat')

        self.text_box = Text(self.root)
        self.text_box.place(relx = 0.05, rely = 0.01, width = 700, height = 600)





        
        self.root.mainloop()

chat = Chat()