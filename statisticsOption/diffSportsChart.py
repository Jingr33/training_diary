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
        self.data_loader = DataLoader()
        # setted sport je z rodičovské třídy
        trainings = self.data_loader.getOneSportTrainings(self.data_loader.trainings, self.setted_sport, first_date, last_date)
        if not trainings:
            return (0, 0, 0)
        chart_content = self._makeChartContent(trainings)
        return chart_content
    
    def _makeChartContent (self, trainings : list) -> list:
        """Vrátí list obsahu pro výseče koláčového grafu."""
        chart_content = SetSport.makeChartContent(trainings, self.setted_sport)
        return chart_content

    def _makeChart(self, chart_content : list) -> None:
        """Rozhodnutí, který typ grafu se má vytvořit a jeho následné vytvoření."""
        chart_type, chart_strings = SetSport.chooseChartType(self.setted_sport)
        if chart_type == "pie":
            self._makePieChart(chart_content, chart_strings)
            self.to_l.grid(row = 2, column = 3, padx = self.entry_padx, pady = self.pady, sticky = "WS")
            self.to_e.grid(row = 3, column = 3, padx = self.entry_padx, pady = self.pady)
        elif chart_type == "bar":
            self._makeBarChart(chart_content, chart_strings)
            self.to_e.grid_forget()
            self.to_l.grid_forget()

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
        self._modifyInterface("pie")
        self._chartPieLabels(chart_strings)

    def _makeBarChart (self, chart_content : list, chart_strings : list) -> None:
        """Vytvoření sloupcového typu grafu."""
        # vytvoření subplotu
        self.figure.clf()
        self.chart = self.figure.add_subplot(111)
        # vykreslení grafu
        num_of_columns = 7
        ind = np.arange(num_of_columns)
        width = 0.6
        bar_plot = self.chart.bar(ind, chart_content, width)
        self._barLabel(bar_plot)
        self._modifyInterface("bar")
        self._chartBarLabels(chart_strings)

    def _editPtc (self, pct, sum) -> str:
        """Formátuje popisek procent na formát (počet, procenta)."""
        count = int(np.round(pct/100*sum))
        return f"{count:d}\n{pct:.0f}%"

    def _modifyInterface (self, chart_type : str) -> None:
        """Nastaví barvy pozadí grafu."""
        self.figure.set_facecolor(colors["dark-gray-2"])
        self.chart.set_facecolor(colors["dark-gray-2"])
        if chart_type == "bar":
            self.chart.spines['top'].set_visible(False)
            self.chart.spines['right'].set_visible(False)
 
    def _chartPieLabels (self, strings : dict) -> None:
        """Nastaví posisky grafu."""
        pad = 20
        self.chart.set_title(strings["title"], pad = pad)

    def _chartBarLabels (self, strings : dict) -> None:
        """Nastaví posisky sloupcového grafu."""
        pad = 10
        self.chart.set_xlabel("Datum")
        self.chart.set_ylabel("Vzdálenost (v km)")
        periods = self.data_loader.getPeriods()
        xlabels = self._createColumnXLabels(periods)
        self.chart.set_xticks(range(len(xlabels)))
        self.chart.set_xticklabels(xlabels, rotation='horizontal', fontsize = 8)
        self.chart.set_title(strings["title"], pad = pad)

    def _barLabel (self, plot : object) -> None:
        """Přidá každému sloupci v grafu popisek s číslem jeho četnosti."""
        self.chart.bar_label(plot, label_type='center', fmt = lambda label: self._barLabelFormat(label),
                             fontsize = 9, color = colors["black"])

    def _barLabelFormat (self, label : str) -> str:
        """Naformátuje label sloupce -> pokud je nula nevypíše ho."""
        if label:
            return int(label)
        return ""
    
    def _createColumnXLabels (self, periods : tuple) -> list:
        """Z listu tuplů dat jednotlivých sloupců vytvoří labely pro sloupce."""
        xlabels = [None] * 7
        i = 0
        for period in periods:
            start = General.changeDateForamt(period[0])
            start = start.replace(". ", "/")
            end = General.changeDateForamt(period[1])
            end = end.replace(". ", "/")
            label = start + "\n" + end
            xlabels[i] = label
            i = i + 1
        return xlabels