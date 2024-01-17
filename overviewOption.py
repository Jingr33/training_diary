# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from table import Table
from oneTraining import OneTaining
from configuration import path

class Overview (ctk.CTkFrame):
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)

        # načtení dat po trénincích
        lines = self.laodFileLines(path)

        #pole jednotlivých instancí tréninků
        self.trainings = self.makeTrainings(lines)

        # zavolání framu s vytvořenou tabulkou
        # self.table = Table(self, ...)
        # self.table.pack()



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
            one_training = OneTaining().unlockTheData(one_line)
            trainings.append(one_training)
        return trainings