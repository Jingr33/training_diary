# import knihoven
from tkinter import *
import customtkinter as ctk
import matplotlib.pyplot as plt
from datetime import date
import numpy as np
from datetime import date, datetime
from icecream import ic
# import souborů
from ctkWidgets import Frame, Label, ComboBox
from general import General
from configuration import personal_chart_option, chart_frame_color, personal_data_path, colors


class PersonalDataChart (Frame):
    """Vytvoří bodový graf (propojených lomenou čárou) se změnami osobních údajů o uživateli v čase."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.personal_data = General.loadPersonalData(personal_data_path)
        self.columnconfigure([0,1,2,3,4], weight=1)
        self.figure = None
        self.configure(corner_radius = 10, fg_color = chart_frame_color)
        self.end_date = date.today()
        self.start_date = None
        self._initContent()

    def _initContent (self) -> None:
        """Vytvoří celý obsah framu pro graf zobrazující změnu osobních údajů v čase."""
        self._initWidgets()
        General.pasteChart(self, (0, 1), 5)
        self._createChartContent()

    def _initWidgets (self) -> None:
        """Vytvoří widgety ve framu pro nastavení os grafu."""
        name = Label(self, "Osobní\núdaje", ("Arial", 20, "bold"))
        name.grid(column = 0, row = 0, columnspan = 3, sticky = ctk.W, padx = 10, pady = 15)
        range_l = Label(self, "Období:")
        range_l.grid(column = 3, row = 0, sticky=ctk.E, padx = 5)
        self.var_option = StringVar()
        self.range_cb = ComboBox(self, personal_chart_option, self._setdisplayedPeriod, self.var_option)
        self.range_cb.grid(column = 4, row = 0)
        self.range_cb.configure(width = 100)
        self.var_option.set(personal_chart_option[-1])
        self.range = personal_chart_option[1]

    def _setdisplayedPeriod (self, value) -> None:
        """Nastaví období, které se zobrazí v v grafu."""
        shift = self._setTimeShift(self.var_option.get())
        self.start_date = General.surroundingFirstDate(self.end_date, shift[0], shift[1], 0)
        # nakonec zobrazí znova obsah grafu
        self._createChartContent()

    def _setTimeShift (self, option : str) -> tuple:
        """Vrátí tuple (roky, měsíce), o které se má posunout počáteční datum do minulosti (takže to jsou záporná čísla). Pokud se ná graf nastavit od počátku měření, nastaví se posun 0."""
        if option == personal_chart_option[0]:
            return (0, -3)
        elif option == personal_chart_option[1]:
            return (-1, 0)
        else:
            return (0, 0)

    def _createChartContent (self) -> None:
        """Funkce vytvoří obsah grafu (osy, popisky, body) podle nastaveného období zobrazení."""
        data = self._dataForChart(self.personal_data)
        data = self._selectNeededData(data)
        ic(data)
        self._makeScatterPlot(data)
        self.figure.canvas.draw()

    def _dataForChart (self, data_dict : dict) -> tuple:
        """Převede data ze slovníku do formátu zpracovatelného pro bodový graf."""
        height = General.invertList(data_dict["height"]).tolist()
        mass = General.invertList(data_dict["mass"]).tolist()
        for item in (height, mass):
            for i in range(len(item[1])):
                item[1][i] = General.stringToDate(item[1][i])
        return (height, mass)
    
    def _selectNeededData (self, data : tuple) -> tuple:
        """Vybere data z období vybraného uživatele pro zobrazení."""
        if (not self.start_date) or (self.start_date == self.end_date): return data
        for j in range(len(data)):
            one_list = data[j]
            for i in range(len(one_list[1])):
                if i >= len(one_list[1]): break
                if not General.dateBetween(one_list[1][i], self.start_date, self.end_date):
                    del one_list[0][i]
                    del one_list[1][i]
                    i = i - 1
        return data

    def _makeScatterPlot (self, chart_data : list) -> None:
        """Vytvoření obsahu bodového grafu."""
        # vytvoření subplotu
        self.figure.clf()
        self.chart = self.figure.add_subplot(111)
        # vykreslení grafu
        self.chart.set_ylabel('hmotnost', color = colors["mass-chart"])
        self.chart.tick_params(axis='y', labelcolor=colors["mass-chart"])
        self.chart.scatter(chart_data[0][1], chart_data[0][0], color = colors["mass-chart"])
        # self.chart.plot(chart_data[0][1], chart_data[0][0], color = colors["mass-chart"])

        line_two = self.chart.twinx() 
        line_two.set_ylabel('výška', color=colors["height-chart"])
        line_two.tick_params(axis='y', labelcolor=colors["height-chart"])
        line_two.scatter(chart_data[1][1], chart_data[1][0], color =colors["height-chart"])

        self._modifyChartDesign()

    def _modifyChartDesign (self) -> None:
        """Upraví vzhled grafu."""
        self.chart.set_title("Přehled změn osobních údajů v čase", pad = 20)
        self.chart.set_xlabel('datum')
        self.figure.set_facecolor(colors["dark-gray-2"])
        self.chart.set_facecolor(colors["dark-gray-2"])
        self.chart.spines['top'].set_visible(False)
