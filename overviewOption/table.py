# import knihovem
from tkinter import *
import customtkinter as ctk
from icecream import ic
# import souborů
from overviewOption.oneRow import OneRow
from ctkWidgets import Button
from general import General
from configuration import colors
import globalVariables as GV

class Table (ctk.CTkScrollableFrame):
    """Třída pro vytvoření tabulky přehledu tréninků."""
    def __init__(self, master :ctk.CTkBaseClass, fileData: list):
        super().__init__(master)
        self.master = master
        self.data = fileData
        self.displayed_rows = int(GV.setting["overview-rows"])
        # inicializace grafického rozhraní
        self.initGUI(self.data)

    def initGUI (self, data : list) -> None:
        """Vytvoření grafického rozhraní tabulky."""
        self.section = 1 # kolikátá skupina tréninků se má zobrazit
        self.init_load_more = True # zda se má vytvořit i tlačítko pro zobrazení více tréninků
        self._initContent(data)

    def _initContent (self, data : list) -> None:
        """Vytvoří grafické rozhraní tabulky a jejího nastavení části přehled."""
        # vytvoření řádků tabulky pomocí objektu OneRow
        limit = self._rowsLimits(data)
        for i in range(limit[0], limit[1]):
            one_row = OneRow(self, data[i])
            one_row.pack(side = TOP, fill = ctk.X, padx = 3)
            one_row.configure(height = 40, corner_radius = 0)
            # změna barvy pozadí pro každý druhý řádek
            if i % 2 == 0:
                one_row.configure(fg_color = colors["gray"])
            i = i + 1
            if i >= self.section * self.displayed_rows: # kontrola zda se nevypisuje psóslední řádek sekce
                break
        if self.init_load_more:
            self._initLoadMoreButton()

#################################################################
            # tovypisování hází úplné kraviny, zkus nějak pošéfovat ty dělky training listů
#################################################################

    def _initLoadMoreButton (self) -> None:
        """Metoda vytvoří tlačítko pro načtení více tréninkových řádků v dolní části tabulky."""
        self.load_more = Button(self, "Načíst více", self._addRows)
        self.load_more.pack(side = TOP, pady = 10)
        self.load_more.configure(height = 50, width = 150)

    def _addRows (self) -> None:
        """Přidá další řadky s informacemi o trénincích po kliknutí na tlačítko pro přidání řádků."""
        if self.section * self.displayed_rows < len(self.data):
            self.section = self.section + 1
            General.deleteListWidgets([self.load_more]) # smazání tlačítka
            self._initContent(self.data)
            if self.init_load_more: # pokud už není co načíst, tlačítko se nevygeneruje
                self._initLoadMoreButton()

    def _rowsLimits (self, training_data : list) -> tuple:
        """Vypočítá rozpětí indexů tréniků, které se mají vypsat. Vrátí tuple krajních hodnot.
        Pokud je rozsah tréninků u konce, nastaví se hodnota, která zamezí vytvoření tlačítka pro více tréninků."""
        lower_limit = (self.section - 1) * self.displayed_rows
        upper_limit = self.section * self.displayed_rows
        if upper_limit > len(training_data): # aby nebyla přesažena velikost listu tréninků
            upper_limit = len(training_data)
            self.init_load_more = False # aby se nevytvářelo tlačítko pro více tréninků
        return (lower_limit, upper_limit)

