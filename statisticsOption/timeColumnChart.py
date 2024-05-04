#import knihoven
from tkinter import * 
import customtkinter as ctk
import matplotlib.pyplot as plt
from dateutil.relativedelta import *
from numpy import arange
from math import floor
# import souborů
from statisticsOption.dataLoader import DataLoader
from statisticsOption.barChart import BarChart
from general import General
from configuration import colors


class TimeColumnChart (BarChart):
    """Frame s grafem ukazující počet odsportovaných minut v jednotlivých obdobích."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.time_range_func = [self._dailyColumn, self._weeklyColumn, self._monthlyColumn, self._yearlyColumn]
        self.actual_date = self.today
        self.figure = None
        self.chart = None # proměnná pro graf
        self.xdata = None # popisky osy x (data)
        self._initBarChartFrame(self._updateChart, "Čas")
        self._updateChart()

    def _updateChart(self, value = None) -> None:
        """Metoda pro přegenerování grafu při změně vstupních dat."""
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
        """Spočátá odcvičené minuty v jednotlivých obdobích."""
        period_minutes = [0] * len(periods)
        for i in range(len(periods)): # pro každou periodu (sloupec)
            for training in periods[i]: # trénink ve sloupci
                try:
                    time = int(training.time)
                except:
                    time = 0
                period_minutes[i] = period_minutes[i] + time
        return period_minutes

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
        bar_plot = self.chart.bar(ind, transp_data, width, color = colors["light-blue"])
        self._barLabel(bar_plot)
        self._modifyDesign()
        self._chartLabels()

    def _barLabel (self, plot : object) -> None:
        """Přidá každému sloupci v grafu popisek s číslem jeho četnosti."""
        self.chart.bar_label(plot, label_type='center', fmt = lambda label: self._barLabelFormat(label), fontsize = 8, color = colors["black"])

    def _barLabelFormat (self, label : str) -> str:
        """Naformátuje label sloupce -> pokud je nula nevypíše ho."""
        hours = floor(int(label) / 60)
        minutes = int(label) % 60
        text = ""
        if hours:
            text = text + str(hours) + " hod"
        if minutes:
            text = text + "\n" + str(minutes) + " min"
        return text

    def _chartLabels (self) -> None:
        """Nastaví popisky grafu."""
        self.chart.set_xlabel("Datum")
        self.chart.set_ylabel("Celkový čas pohybu")
        self.chart.set_title("Množství sportovní aktivity", pad = 10)
        self.chart.set_xticks(range(len(self.xdata)))
        self.chart.set_xticklabels(self.xdata, rotation='horizontal', fontsize = 8)

    def _modifyDesign (self) -> None:
        """úUprva vzhledu os grafu."""
        self.chart.spines['top'].set_visible(False)
        self.chart.spines['right'].set_visible(False)
        self.figure.set_facecolor(colors["dark-gray-2"])
        self.chart.set_facecolor(colors["dark-gray-2"])