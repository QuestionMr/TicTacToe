import logging
from tkinter import *
from tkinter import ttk

class TextHandler(logging.StreamHandler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget

    def __init__(self, text):
        logging.StreamHandler.__init__(self)
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        self.text.config(state="normal")
        self.text.insert("end", msg + "\n")
        self.flush()
        self.text.config(state="disabled")