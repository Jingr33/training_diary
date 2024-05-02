#import knihoven
import customtkinter as ctk
from tkinter import *
#import souborů
from ctkWidgets import Frame, Entry, Label

class FilterTime (Frame):
    """Frame pro filtrování času."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.var_from = StringVar()
        self.var_to = StringVar()
        # vytvoření zadávacích polí pro filtrování času
        from_l = Label(self, "Od:")
        from_l.grid(row = 0, column = 0)
        from_l.configure(font= ("Arial", 12))
        from_e = Entry(self, self.var_from)
        from_e.grid(row=0, column=1, ipadx=2, ipady=1)
        from_e.configure(width = 35)
        to_l = Label(self, "Do:")
        to_l.grid(row=1, column=0)
        to_l.configure(font= ("Arial", 12))
        to_e = Entry(self, self.var_to)
        to_e.grid(row=1, column=1, ipadx=2, ipady=1)
        to_e.configure(width = 35)

    def filtered(self):
        """Vrátí hodnoty zakliknuté ve filtru času."""
        values = [self.var_from.get(), self.var_to.get()]
        return values
