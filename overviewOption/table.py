# import knihovem
from tkinter import *
import customtkinter as ctk
# import souborů
from overviewOption.oneRow import OneRow
from overviewOption.legend import Legend
from configuration import colors

class Table (ctk.CTkScrollableFrame):
    """Třída pro vytvoření tabulky přehledu tréninků."""
    def __init__(self, master :ctk.CTkBaseClass, fileData: list):
        super().__init__(master)
        self.data = fileData # cesta souboru který načítám do tabulky
        # inicializace grafického rozhraní
        self.initContent(self.data)

    def initContent (self, data : list) -> None:
        """Vytvoří grafické rozhraní tabulky a jejího nastavení části přehled."""
        # vytvoření řádků tabulky pomocí objektu OneRow
        i = 0
        for training in data:
            one_row = OneRow(self, training)
            one_row.pack(side = TOP, fill = ctk.X, padx = 3)
            one_row.configure(height = 40, corner_radius = 0)
            # změna barvy pozadí pro každý druhý řádek
            if i % 2 == 0:
                one_row.configure(fg_color = colors["gray"])
            i = i + 1
