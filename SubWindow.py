from tkinter import *
class SubWindow(Tk):
    text = 0
    def __init__(self, parent):
        Tk.__init__(self,parent)
        self.parent = parent

        self.text = Text(self)