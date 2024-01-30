# import knihoven
from tkinter import *
import customtkinter as ctk
from CTkToolTip import *
# import souborů
from ctkWidgets import Label
from configuration import sport_color

class OneActivity (Label):
    """Uchovává informace o aktivitách v jednotlivých dnech a vytváří pruh v náhledovém
    kalendáři (v nastavení cyklického tréninkového plánu)."""
    def __init__ (self, master : ctk.CTkBaseClass, selected_sport : str, details : tuple):
        font = ("Arial", 13)
        super().__init__(master, selected_sport, font)
        # barva pozadí
        self.configure(fg_color = sport_color[selected_sport], corner_radius = 5)

        # zpracování přijatých dat
        self._loadData(selected_sport, details)

        #TODO nakonec se při uložení sem musí uložit taky pořadí dne, v tréninkovém plánu

    def _loadData(self, selected_sport, details) -> None:
        """Zpracuje získaná data a uloží je do listu."""
        self.sport = selected_sport
        # uložení základních údajů do listu
        self.data = [0, self.sport] # -> 0 je místo pro pořadí dne
        #přepsání dat s tuplu do listu za základní údaje 
        for item in details:
            self.data.append(item)

    def bindWithDay(self, day_number : int) -> None:
        """Metoda přidá do listu s daty o tréniku pořadí dne, ve kterém je."""
        self.data[0] = day_number