# import knihovem
from tkinter import *
import customtkinter as ctk
# import souborů

class Table (ctk.CTkFrame):
    """Třída pro vytvoření tabulky přehledu tréninků."""
    def __init__(self, master :ctk.CTkBaseClass, fileData: list):
        super().__init__(master)
        self.data = fileData # cesta souboru který načítám do tabulky

                