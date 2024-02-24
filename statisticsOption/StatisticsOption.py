# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from statisticsOption.dataLoader import DataLoader
from statisticsOption.sportColumnChart import SportColumnChart
from statisticsOption.timeColumnChart import TimeColumnChart
from statisticsOption.sportRatioChart import SportRatioChart
from statisticsOption.diffSportsChart import DiffSportsChart


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
        sport_chart = SportColumnChart(self) # graf poměru vykonaných sportů - sloupcový
        sport_chart.grid(column = 0, row = 0,ipadx = 5, ipady = 5, padx = 5, pady = 5, sticky = "NWSE")
        sport_ratio_chart = SportRatioChart(self) # graf poměru vykonaných tréninků - koláčový 
        sport_ratio_chart.grid(column = 1, row = 0,ipadx = 8, ipady = 8, padx = 9, pady = 9, sticky = "NWSE")
        time_chart = TimeColumnChart(self) # odtrénovaný čas za období
        time_chart.grid(column = 0, row = 1,ipadx = 5, ipady = 5, padx = 9, pady = 9, sticky = "NWSE")
        sport_chart = DiffSportsChart(self) # graf poměru vykonaných sportů
        sport_chart.grid(column = 1, row = 1,ipadx = 5, ipady = 5, padx = 5, pady = 5, sticky = "NWSE")

    def _dataLoader (self) -> None:
        """Zavolání objektu načítajícího tréninková data."""
        self.data_loader = DataLoader()