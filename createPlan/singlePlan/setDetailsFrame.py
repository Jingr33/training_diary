# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from ctkWidgets import Frame


class SetDetailsFrame (Frame):
    """Vytvoří frame v nastavení jednoduchého tréninkového plánu pro nastavení podrobností 
    jednotlivých tréninků."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)