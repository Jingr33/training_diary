# import knihovem
from tkinter import *
import customtkinter as ctk
#import souborů
from configuration import legend, colors, sorting_bg, sorting_text_color
from ctkWidgets import Label

class Legend (ctk.CTkFrame):
    """Třída pro vytvoření framu s legendou."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.number_of_sorts = 0 # počet sloupců vybraných zároveň pro třídění
        self.button_sort_level = {
            "b_date" : 0,
            "b_sport" : 0,
            "b_time" : 0,
            "b_details" : 0,
        }
        # nastavení barvy framu
        self.configure(fg_color = colors["dark-gray"])

        # vytvoření labelů s popisky
        self.date_l = Label(self, legend[0])
        self.date_l.pack(side=LEFT, fill = ctk.Y, padx = 8, pady = 8)
        self.date_l.configure(width=100, height=45, font=("Arial", 14, 'bold'), corner_radius = 6)

        self.sport_l = Label(self, legend[1])
        self.sport_l.pack(side=LEFT, fill = ctk.Y, padx = 8, pady = 8)
        self.sport_l.configure(width=110, height=45, anchor=ctk.W, font=("Arial", 14, 'bold'), corner_radius = 6)

        self.time_l = Label(self, legend[2])
        self.time_l.pack(side=LEFT, fill = ctk.Y, padx = 8, pady = 8)
        self.time_l.configure(width=70, height=45, anchor=ctk.W, font=("Arial", 14, 'bold'), corner_radius = 6)

        self.details_l = Label(self, legend[3])
        self.details_l.pack(side=LEFT, fill = ctk.Y, padx = 8, pady = 8)
        self.details_l.configure(width=250, height=45, anchor=ctk.W, font=("Arial", 14, 'bold'), corner_radius = 6)

        # eventy pro třídění dat podle položky
        self.date_l.bind("<Button-1>", self._dateSort)
        self.sport_l.bind("<Button-1>", self._sportSort)
        self.time_l.bind("<Button-1>", self._timeSort)
        self.details_l.bind("<Button-1>", self._detailsSort)

    def _dateSort (self, value) -> None:
        """Nastaví správný stupeň třídění dané položky (resp. barvu) 
        a vytřídí data vhodným způsobem."""
        #nastavení stupně třídění
        self._setSortingLevel("b_date")
        # vytřídění dat

    def _sportSort (self, value) -> None:
        """Nastaví správný stupeň třídění dané položky (resp. barvu) 
        a vytřídí data vhodným způsobem."""
        #nastavení stupně třídění
        self._setSortingLevel("b_sport")
        # vytřídění dat

    def _timeSort (self, value) -> None:
        """Nastaví správný stupeň třídění dané položky (resp. barvu) 
        a vytřídí data vhodným způsobem."""
        #nastavení stupně třídění
        self._setSortingLevel("b_time")
        # vytřídění dat

    def _detailsSort (self, value) -> None:
        """Nastaví správný stupeň třídění dané položky (resp. barvu) 
        a vytřídí data vhodným způsobem."""
        #nastavení stupně třídění
        self._setSortingLevel("b_details")
        # vytřídění dat

    def _setSortingLevel (self, button : str) -> None:
        """Nastaví uroveň třídění jednotlivým sloupcům."""
        # zvýší se celková úroveň třídění (počet tříděných sloupců)
        self._buttonSortLevelUpdate(button)
        print(self.number_of_sorts)
        print(self.button_sort_level)
        # nastavení barev pozadí legendy sloupců
        self._setLabelBg()


    def _buttonSortLevelUpdate (self, button : str) -> None:
        """Aktualizuje úroveň třídění jednotlivého tlačítka po jeho stisknutí."""
        # počet aktivovaných třídění sloupců
        active_elems = self._activatedElements()
        # aktualizace urovní sloupců
        self._updateLevelValues(button, active_elems)

    def _activatedElements (self) -> int:
        """Získá počet aktivovaných sloupců. Vrátí int počtu setříděných sloupců."""
        sorted_elements = 0
        for element in self.button_sort_level:
            if self.button_sort_level[element]:
                sorted_elements = sorted_elements + 1
        return sorted_elements
    
    def _updateLevelValues (self, button : str, active_elems : int) -> None:
        """Aktualizuje hodnoty úrovní jednotlivých položek/slupců."""
        if self.button_sort_level[button]: # pokud má nějakou úroveň různou od 0
            self._delevelSorting(button, active_elems)
            self._updateOtherElemes(button)
        else: # pokud má sloupec úroveň 0
            self._activateSorting(button)
            self._delevelAllElems(button)

    def _activateSorting (self, button : str) -> None:
        """Dá stiknutý sloupec na hodnotu 1 (nejvyšší level). Zvýší celkový počet tříděných sloupců."""
        self.number_of_sorts = self.number_of_sorts + 1 # zvýšení celkového počtu třáděných sloupců
        self.button_sort_level[button] = self.button_sort_level[button] + 1 # zvýšení vlastního levelu na maximum

    def _delevelSorting (self, button : str, active_elems : int) -> None:
        """Metoda sníží level třídění položky/sloupce, pokud už předtím nějakou úroveň měla."""
        self.button_sort_level[button] = self.button_sort_level[button] + 1 # snížení úrovně levelu
        # pokud úroveň přesáhne celkový počet tříděných položek, vynuluje se
        if self.button_sort_level[button] > active_elems:
            self.button_sort_level[button] = 0
            # změna celkového počtu tříděných sloupců
            self.number_of_sorts = self.number_of_sorts - 1

    def _delevelAllElems (self, button : str) -> None:
        """Sníží všechny již zakliknuté sloupce na nižší level třídění."""
        for element in self.button_sort_level:
            if element != button:
                if self.button_sort_level[element] != 0:
                    self.button_sort_level[element] = self.button_sort_level[element] + 1

    def _updateOtherElemes (self, button : str) -> None:
        """Updatuje levely všech ostatních položek při snížení levelu jedné položky."""
        for element in self.button_sort_level:
            # pokud je level stejný jako level změněné položky, zvýší se 
            if element != button:
                if (self.button_sort_level[element] == self.button_sort_level[button] 
                    and self.button_sort_level[button] != 0):
                    self.button_sort_level[element] = self.button_sort_level[element] - 1
            # pokud byl level vyšší než je level měněné položky, zůstane stejný

    def _setLabelBg (self) -> None:
        """Nastaví barvy pozadí labelům v legendě podle úrovně třídění."""
        self.date_l.configure(fg_color = sorting_bg[self.button_sort_level["b_date"]], 
                              text_color = sorting_text_color[self.button_sort_level["b_date"]])
        self.sport_l.configure(fg_color = sorting_bg[self.button_sort_level["b_sport"]], 
                              text_color = sorting_text_color[self.button_sort_level["b_sport"]])
        self.time_l.configure(fg_color = sorting_bg[self.button_sort_level["b_time"]], 
                              text_color = sorting_text_color[self.button_sort_level["b_time"]])
        self.details_l.configure(fg_color = sorting_bg[self.button_sort_level["b_details"]], 
                              text_color = sorting_text_color[self.button_sort_level["b_details"]])