# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from ctkWidgets import Frame


class Setting (Frame):
    """Načte frame při zvolení "Možnosti" v horním baneru."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.configure(corner_radius = 8)
        