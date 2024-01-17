# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from overviewOption.table import Table
from oneTraining import OneTraining
from configuration import path
from overviewOption.filterFrame import FilterFrame

class Overview (ctk.CTkFrame):
    """Třída pro vyvolání obsahu při zvolení možnosti přehled v menu."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)

        # načtení dat po trénincích
        lines = self.laodFileLines(path)

        #pole jednotlivých instancí tréninků
        self.trainings = self.makeTrainings(lines)

        # část pro filtry - vytvoření filtrovacího rozhraní
        self.filter_frame = FilterFrame(self, self.trainings)
        self.filter_frame.pack(side=TOP, fill=ctk.X, expand=False)
        self.filter_frame.configure(corner_radius = 0)

        # funkce pro vytvoření tabulky
        self._initTable(self.trainings)

        self.filter_frame.filter_button.bind('<Button-1>', self._initFiltering)


    def _initTable(self, trainings):
        """Metoda iniciuje vytvoření tabulky přehledu tréninků."""
        # zavolání framu s vytvořenou tabulkou
        self.table = Table(self, trainings)
        self.table.pack(fill = ctk.BOTH, expand = True)
        self.table.configure(corner_radius = 0)

    def _initFiltering(self, master):
        # získání dat z filtrování
        filtered_trainings = self.filter_frame.getData()

        # nová iniciace tabulky s tréninky s filtrovanými daty
        if self.table:
            self.table.destroy()
        self._initTable(filtered_trainings)


    def laodFileLines(self, path):
        """Metoda pro načtení dat ze souboru po jednotlivých trénincích."""
        # načtení všech dat do pole po jednotlivých řádcích
        with open(path, 'r') as f:
            lines = f.readlines()
        return lines
    
    def makeTrainings (self, data_lines):
        """Metoda vytvoří pole jednotlivých tréninků."""
        trainings = []
        for one_line in data_lines:
            one_training = OneTraining("load", one_line)
            trainings.append(one_training)
        return trainings