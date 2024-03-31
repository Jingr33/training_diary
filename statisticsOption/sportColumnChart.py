# import knihoven
from tkinter import * 
import customtkinter as ctk
import matplotlib.pyplot as plt
from dateutil.relativedelta import *
from numpy import arange
# import souborů
from statisticsOption.dataLoader import DataLoader
from statisticsOption.barChart import BarChart
from general import General
from configuration import sport_color, colors
import globalVariables as GV

class SportColumnChart (BarChart):
    """Frame s grafem ukazující poměr vykonaných sportů."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.time_range_func = [self._dailyColumn, self._weeklyColumn, self._monthlyColumn, self._yearlyColumn]
        self.actual_date = self.today
        self.figure = None
        self.chart = None # proměnná pro graf
        self.xdata = None # popisky osy x (data)
        self._initBarChartFrame(self._updateChart, "Sporty")
        self._updateChart()

    def _updateChart(self, value = None) -> None:
        """Funkce pro přegenerování grafu při změně vstupních dat."""
        self._chartTrigger(self._getTrainings, self._makeChart)

    def _getTrainings (self, date_tuples : list) -> None:
        """Vygeneruje z tréninků data pro graf."""
        trainings = self._getTrainingsInPeriod(date_tuples)
        chart_data = self._numberOfTrainings(trainings)
        return chart_data

    def _getTrainingsInPeriod (self, date_tuples : list) -> list:
        """Vrátí list listů s tréninky pro každou časovou periodu."""
        data_loader = DataLoader()
        training_lists = [None] * len(date_tuples)
        i = 0
        for date_tuple in date_tuples:
            one_period = data_loader.getTrainingsInDate(data_loader.trainings, date_tuple[0], date_tuple[1])
            training_lists[i] = one_period
            i = i + 1
        return training_lists
    
    def _numberOfTrainings (self, periods : list) -> list:
        """Spočítá, kolik tréninků v zadaném listu náleželo jednotlivým sportům.
        Vrátí list listů s počty tréninků."""
        periods_numbers = []
        for period in periods:
            period_numbers = self._periodNumbers(period)
            periods_numbers.append(period_numbers)
        return periods_numbers

    def _makeChart (self, data : list) -> None:
        """Vytvoří nový obsah grafu."""
        # vytvoření subplotu
        self.figure.clf()
        self.chart = self.figure.add_subplot(111)
        # vykreslení grafu
        num_of_columns = 7
        ind = arange(num_of_columns)
        transp_data = General.invertList(data)
        width = 0.6
        for i in range(len(data[0])):
            if i == 0:
                bar_plot = self.chart.bar(ind, transp_data[i], width, color = sport_color[GV.sport_list[i]])
            else:
                bar_plot = self.chart.bar(ind, transp_data[i], width, bottom = transp_data[0], color = sport_color[GV.sport_list[i]])
            self._barLabel(bar_plot, transp_data[i])
        self._modifyInterface()
        self._chartLabels()

    def _barLabel (self, plot : object, data : list) -> None:
        """Přidá každému sloupci v grafu popisek s číslem jeho četnosti."""
        self.chart.bar_label(plot, label_type='center', fmt = lambda label: self._barLabelFormat(label),
                             fontsize = 9, color = colors["black"])

    def _barLabelFormat (self, label : str) -> str:
        """Naformátuje label sloupce -> pokud je nula nevypíše ho."""
        if label:
            return int(label)
        return ""

    def _chartLabels (self) -> None:
        """Nastaví popisky grafu."""
        self.chart.legend(GV.sport_list, facecolor = colors["dark-gray-2"], frameon=False)
        self.chart.set_xlabel("Datum")
        self.chart.set_ylabel("Počet tréninků")
        self.chart.set_title("Počet typů tréninků za období", pad = 10)
        self.chart.set_xticks(range(len(self.xdata)))
        self.chart.set_xticklabels(self.xdata, rotation='horizontal', fontsize = 8)

    def _modifyInterface (self) -> None:
        """úUprva vzhledu os grafu."""
        self.chart.spines['top'].set_visible(False)
        self.chart.spines['right'].set_visible(False)
        self.figure.set_facecolor(colors["dark-gray-2"])
        self.chart.set_facecolor(colors["dark-gray-2"])
