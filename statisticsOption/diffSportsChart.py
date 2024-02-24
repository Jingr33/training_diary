#importy knihoven
from tkinter import *
import customtkinter as ctk
from datetime import date
import numpy as np
#importy souborů
from statisticsOption.pieChart import PieChart
from statisticsOption.dataLoader import DataLoader
from sports.setSport import SetSport
from general import General
from configuration import colors

class DiffSportsChart (PieChart):
    """Třída pro vytvoření grafu s s pordrobnosti tréninků jednoho sportovního typu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.error_l = None

        self._initPieChartFrame("Podrobnosti", self._getTrainings, self._makeChart, True)
        self._updateChart(self._getTrainings, self._makeChart)

    def _getTrainings (self, first_date : date, last_date : date) -> list:
        """Vrátí listů legend jednotlivých výsečí a počtů sportů pro jednotlivé tréninky."""
        #načtení listu tréninků
        data_loader = DataLoader()
        # setted sport je z rodičovké třídy
        trainings = data_loader.getOneSportTrainings(data_loader.trainings, self.setted_sport, first_date, last_date)
        if not trainings:
            return (0, 0, 0)
        chart_content = self._makeChartContent(trainings)
        return chart_content
    
    def _makeChartContent (self, trainings : list) -> list:
        """Vrátí list obsahu pro výseče koláčového grafu."""
        sport = trainings[0].sport
        chart_content = SetSport.makeChartContent(trainings, sport)
        return chart_content

    def _makeChart(self, chart_content : list) -> None:
        """Rozhodnutí, který typ grafu se má vytvořit a jeho následné vytvoření."""
        chart_type, chart_strings = SetSport.chooseChartType(self.setted_sport)
        if chart_type == "pie":
            self._makePieChart(chart_content, chart_strings)
        elif chart_type == "bar":
            self._makeBarChart(chart_content, chart_strings)

    def _makePieChart (self, chart_content : list, chart_strings : dict) -> None:
        """Vytvoření koláčového typu grafu."""
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
        self._chartLabels(chart_strings)

    def _makeBarChart (self, chart_content : list, chart_strings : list) -> None:
        """Vytvoření sloupcového typu grafu."""
        ...

    def _editPtc (self, pct, sum) -> str:
        """Formátuje popisek procent na formát (počet, procenta)."""
        count = int(np.round(pct/100*sum))
        return f"{count:d}\n{pct:.0f}%"

    def _modifyInterface (self) -> None:
        """Nastaví barvy pozadí grafu."""
        self.figure.set_facecolor(colors["dark-gray-2"])
        self.chart.set_facecolor(colors["dark-gray-2"])

    def _chartLabels (self, strings : dict) -> None:
        """Nastaví posisky grafu."""
        self.chart.set_title(strings["title"], pad = 20)
