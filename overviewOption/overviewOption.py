# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from overviewOption.table import Table
from oneTraining import OneTraining
from configuration import trainings_path
from overviewOption.filterFrame import FilterFrame
from overviewOption.legend import Legend
from overviewOption.sorting import Sorting


class Overview (ctk.CTkFrame):
    """Třída pro vyvolání obsahu při zvolení možnosti přehled v menu."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.filtered_trainings = None

        # načtení dat po trénincích
        lines = self.laodFileLines(trainings_path)

        #pole jednotlivých instancí tréninků
        self.trainings = self.makeTrainings(lines)

        #vytvoření filtrovacího rozhraní
        self._initFilters()
        # vytvoření legendy tabulky
        self._initLegend()
        # funkce pro vytvoření tabulky
        self._initTable(self.trainings)

    def Filtering(self) -> None:
        """Spustí se při stisknutí filtrovaní dat ve framu filtrování. 
        Načte vybrané tréninky, vytvoří novou tabulku."""
        # získání dat z filtrování
        self.filtered_trainings = self.filter_frame.getData()
        # nová iniciace tabulky s vyfiltrovanými daty
        for widget in self.table.winfo_children():
            widget.destroy()
        self.table.initContent(self.filtered_trainings)

    def _initFilters (self) -> None:
        """Vytvoří scrollable frame s filtrovacím rozhraním."""
        self.filter_frame = FilterFrame(self, self.trainings)
        self.filter_frame.pack(side=TOP, fill=ctk.X, expand=False)
        self.filter_frame.configure(corner_radius = 0)


    def _initLegend (self) -> None:
        """Vytvoří frame s legendou tabulky."""
        self.legend = Legend(self)
        self.legend.pack(side=TOP, fill = ctk.X, padx = 0, pady=0)
        self.legend.configure(height = 45, corner_radius = 0)


    def _initTable(self, trainings) -> None:
        """Metoda iniciuje vytvoření tabulky přehledu tréninků."""
        # zavolání framu s vytvořenou tabulkou
        self.table = Table(self, trainings)
        self.table.pack(fill = ctk.BOTH, expand = True)
        self.table.configure(corner_radius = 0)

    def laodFileLines(self, path) -> list:
        """Metoda pro načtení dat ze souboru po jednotlivých trénincích."""
        # načtení všech dat do pole po jednotlivých řádcích
        with open(path, 'r') as f:
            lines = f.readlines()
        return lines
    
    def makeTrainings (self, data_lines) -> list:
        """Metoda vytvoří pole jednotlivých tréninků."""
        trainings = []
        for one_line in data_lines:
            one_training = OneTraining(self, "load", one_line)
            trainings.append(one_training)
        return trainings
    
    def sortData (self) -> None:
        """Setřídění tréninků v tabulce urovní položek pro třídění."""
        # úrovně třídění
        sort_levels = self.legend.getSortLevels()
        # list vyfiltrovaných/nevyfiltrovaných tréninků 
        trainings = self.getActualTrainings()
        # vyfiltrování dat
        sorting = Sorting(trainings, sort_levels)
        sorted_trainings = sorting.GetSortedTrainings()
        # přegenerování tréninků v tabulce
        self._resortTable(sorted_trainings)

    def _resortTable (self, sorted_trainings : list) -> None:
        """Ze vstupních dat přegeneruje obsah tabulky a setřídí data 
        podle uživatelových požadavků."""
        for widget in self.table.winfo_children():
            widget.destroy()
        self.table.initContent(sorted_trainings)


    def getActualTrainings (self) -> list:
        """Vrátí list vyfiltrovaných (resp. nevyfiltrovaných) tréninků
        aktuálně zvolených uživatelem."""
        if self.filtered_trainings:
            return self.filtered_trainings
        return self.trainings