# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from statisticsOption.sportChart import SportChart
from statisticsOption.dataLoader import DataLoader


class Statistics (ctk.CTkScrollableFrame):
    """Frame zobrazující statistiky tréninků."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.configure(corner_radius = 8)
        self.columnconfigure([0,1], weight = 1)
        self.rowconfigure([0,1], weight = 1)
        self.frame_corner = 8
        self._initCharts()
        self._dataLoader()

    def _initCharts(self) -> None:
        """Vytvoření framů s grafy."""
        sport_chart = SportChart(self) # graf poměru vykonaných sportů
        sport_chart.grid(column = 0, row = 0,ipadx = 5, ipady = 5, padx = 5, pady = 5)
        sport_chart.configure(corner_radius = 8)

        # testovací framy
        sport_chart = SportChart(self) # graf poměru vykonaných sportů
        sport_chart.grid(column = 0, row = 1,ipadx = 8, ipady = 8, padx = 9, pady = 9)
        sport_chart = SportChart(self) # graf poměru vykonaných sportů
        sport_chart.grid(column = 1, row = 0,ipadx = 5, ipady = 5, padx = 9, pady = 9)
        sport_chart = SportChart(self) # graf poměru vykonaných sportů
        sport_chart.grid(column = 1, row = 1,ipadx = 5, ipady = 5, padx = 5, pady = 5)

    def _dataLoader (self) -> None:
        """Zavolání objektu načítajícího tréninková data."""
        self.data_loader = DataLoader()