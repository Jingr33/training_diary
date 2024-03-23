# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from ctkWidgets import Frame

class LandingPage (Frame):
    """Třída generující widgety na landing page při spuštění aplikace."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        