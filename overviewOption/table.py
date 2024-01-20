# import knihovem
from tkinter import *
import customtkinter as ctk
# import souborů
from overviewOption.oneRow import OneRow
from overviewOption.legend import Legend

class Table (ctk.CTkScrollableFrame):
    """Třída pro vytvoření tabulky přehledu tréninků."""
    def __init__(self, master :ctk.CTkBaseClass, fileData: list):
        super().__init__(master)
        self.data = fileData # cesta souboru který načítám do tabulky
        # inicializace grafického rozhraní
        self.initGUI()

    def initGUI (self):
        """Vytvoří grafické rozhraní tabulky a jejího nastavení části přehled."""
        # vytvoření legendy tabulky
        legend = Legend(self)
        legend.pack(side=TOP, fill = ctk.X, padx = 3)
        legend.configure(height = 45, corner_radius = 0)

        # vytvoření řádků tabulky pomocí objektu OneRow
        i = 0
        for training in self.data:
            one_row = OneRow(self, training)
            one_row.pack(side = TOP, fill = ctk.X, padx = 3)
            one_row.configure(height = 40, corner_radius = 0)
            # změna barvy pozadí pro každý druhý řádek
            if i % 2 == 0:
                one_row.configure(fg_color = "#333333")
            i = i + 1
