# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from ctkWidgets import Frame


class SportSelectionFrame (Frame):
    """Vytvoří frame pro vybraní nebo odebraání sportů v nastavení aplikace."""
    def __init__(self, master : ctk.CTkBaseClass):
        self.master = master
        super().__init__(master)