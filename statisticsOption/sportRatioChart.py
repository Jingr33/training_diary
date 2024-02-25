# import knihoven
from tkinter import *
import customtkinter as ctk
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
# import souborů
from statisticsOption.pieChart import PieChart
from statisticsOption.dataLoader import DataLoader
from configuration import colors, sport_color

class SportRatioChart (PieChart):
    """Třída pro vytvoření koláčového grafu s počty tréninků jednotlivých sportů v daném období."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        # vytvoření framu s widgetami
        self._initPieChartFrame("Sporty", self._getTrainings, self._makeChart)
        self._updateChart(self._getTrainings, self._makeChart)

    def _getTrainings (self, first_date : date, last_date : date) -> list:
        """Vrátí listů legend jednotlivých výsečí a počtů sportů pro jednotlivé tréninky."""
        #načtení listu tréninků
        data_loader = DataLoader()
        trainings = data_loader.getTrainingsInDate(data_loader.trainings, first_date, last_date)
        chart_content = self._makeChartContent(trainings)
        return chart_content

    def _makeChartContent (self, trainings) -> list:
        """Vytvoří list údajů o počtech tréninků a list názvů jednotlivých výsečí pro graf."""
        sport_dict = self._sportCountDict(trainings)
        chart_content = self._chartContentLists(sport_dict)
        return chart_content

    def _sportCountDict (self, trainings : list) -> dict:
        """Ze zadaných tréninnků vytvoří slovník, kde klíč je název sportu a hodnota je počet 
        tréninků tohoto typu."""
        sport_count = {}
        for training in trainings:
            if training.sport in sport_count:
                sport_count[training.sport] = sport_count[training.sport] + 1
            else:
                sport_count[training.sport] = 1
        return sport_count
        
    def _chartContentLists (self, sport_dict : dict) -> list:
        """Ze slovníku (klíč : název sportu, hodnota: počet tréninků sportu) vytvoří 2 listy.
        \n 1) legenda sportů,
        \n 2) počty tréninků sportů.
        \n 3) barvy přiřazené každému sportu."""
        legend = sport_dict.keys()
        count = sport_dict.values()
        colors = []
        for sport in legend:
            colors.append(sport_color[sport])
        return (legend, count, colors)
            
    def _makeChart (self, chart_content : tuple) -> None:
        """Vytvoří koláčový graf poměru počtu tréninků naležících jednotlivým sportům za období."""
        legend, counts, color = chart_content
        # vytvoření subplotu
        self.figure.clf()
        self.chart = self.figure.add_subplot(111)
        # vytvoření grafu
        explode = [0.035] * len(legend)
        train_sum = sum(counts)
        self.chart.pie(counts, labels = legend, startangle = 90, explode = explode, colors = color, 
                       radius = 1.2, autopct = lambda pct: self._editPtc(pct, train_sum), textprops = {'fontsize' : 11})
        self._modifyInterface()
        self._chartLabels()

    def _editPtc (self, pct, sum) -> str:
        """Formátuje popisek procent na formát (počet, procenta)."""
        count = int(np.round(pct/100*sum))
        return f"{count:d}\n{pct:.0f}%"

    def _modifyInterface (self) -> None:
        """Nastaví barvy pozadí grafu."""
        self.figure.set_facecolor(colors["dark-gray-2"])
        self.chart.set_facecolor(colors["dark-gray-2"])

    def _chartLabels (self) -> None:
        """Nastaví posisky grafu."""
        self.chart.set_title("Počet tréninků za období", pad = 20)
