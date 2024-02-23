# import knihoven
from tkinter import * 
import customtkinter as ctk
from datetime import date
from dateutil.relativedelta import *
#import souborů
from ctkWidgets import Frame, Label, Entry, Button
from general import General
from configuration import chart_frame_color


class PieChart (Frame):
    """Třída pro vytvření koláčového grafu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.columnconfigure([0,3], weight=2)
        self.columnconfigure([1,2], weight = 3)
        self.configure(corner_radius = 10, fg_color = chart_frame_color)
        self.today = date.today()
        self.start_date = self._addPeriod(self.today, (0, 0, -7))
        self.end_date = self.today

    def _initChartFrame (self, chart_name : str, getTrainingsFunc, makeChartFunc) -> None:
        """Vytvoření framu.
        Vstupy: master, funkce s parametry (fisrt_Date, laste_date), vrátí list tréninků. 
        Funkce s parametrem listu dat, vytvoří graf."""
        self.getTrainings = getTrainingsFunc
        self.makeChart = makeChartFunc
        self._initWidgets(chart_name)
        General.pasteChart(self, (0, 1), 4)

    def _initWidgets (self, chart_name : str) -> None:
        """Vytvoření widget v framu grafu."""
        name = Label(self, chart_name, ("Arial", 20, "bold"))
        name.grid(column = 0, row = 0, columnspan = 3, sticky = ctk.W, padx = 10, pady = 15)
        self._initTimeSetting()

    def _initTimeSetting (self) -> None:
        """Vytvoření widget pro nastavení období zobrazovaném v grafu."""
        pady = 1
        button_padx = 1
        entry_padx = 5
        from_l = Label(self, "Od:")
        from_l.grid(row = 2, column = 0, padx = entry_padx, pady = pady, sticky = "WS")

        self.var_from = StringVar()
        from_e = Entry(self, self.var_from)
        from_e.grid(row = 3, column = 0, padx = entry_padx, pady = pady)
        self.var_from.set(General.changeDateForamt(self.start_date))
        from_e.bind('<Return>', self._setStartDate)
        from_e.bind('<FocusOut>', self._setStartDate)

        week = Button(self, "Týden", self._setWeekPeriod)
        week.grid(row = 2, column = 1, padx = button_padx, pady = pady, sticky = "E")
        month = Button(self, "Měsíc", self._setMonthPeriod)
        month.grid(row = 2, column = 2, padx = button_padx, pady = pady, sticky = "W")
        three_month = Button(self, "3 měsíce", self._setThreeMonthPeriod)
        three_month.grid(row = 3, column = 1, padx = button_padx, pady = pady, sticky = "E")
        year = Button(self, "Rok", self._setYearPeriod)
        year.grid(row = 3, column = 2, padx = button_padx, pady = pady, sticky = "W")

        to_l = Label(self, "Do:")
        to_l.grid(row = 2, column = 3, padx = entry_padx, pady = pady, sticky = "WS")

        self.var_to = StringVar()
        to_e = Entry(self, self.var_to)
        to_e.grid(row = 3, column = 3, padx = entry_padx, pady = pady)
        self.var_to.set(General.changeDateForamt(self.end_date))
        to_e.bind('<Return>', self._setStartDate)
        to_e.bind('<FocusOut>', self._setStartDate)

    def _setStartDate (self, value) -> None:
        """Nastavení počátečního data."""
        entry_date = self.var_from.get()
        try:
            separator = General.findSeparator(entry_date)
            if separator:
                date_list = entry_date.split(separator)
                self.start_date = date(int(date_list[2]), int(date_list[1]), int(date_list[0]))
                self.var_from.set(General.changeDateForamt(self.start_date))
            else:
                self.var_from.set(General.changeDateForamt(self.start_date))
        except:
            self.var_from.set(General.changeDateForamt(self.start_date))
        self._updateChart(self.getTrainings, self.makeChart)

    def _setEndDate (self, value) -> None:
        """Nastavení koncového data manuálně."""
        entry_date = self.var_to.get()
        try:
            separator = General.findSeparator(entry_date)
            if separator:
                date_list = entry_date.split(separator)
                self.start_date = date(int(date_list[2]), int(date_list[1]), int(date_list[0]))
                self.var_from.set(General.changeDateForamt(self.start_date))
            else:
                self.var_from.set(General.changeDateForamt(self.start_date))
        except:
            self.var_from.set(General.changeDateForamt(self.start_date))
        self._updateChart(self.getTrainings, self.makeChart)

    def _setWeekPeriod (self) -> None:
        """Nastaví týdenní obdodí od počátečního dne při kliknutí na tlačítko týden."""
        self.var_from.set(General.changeDateForamt(self.start_date))
        self.end_date = self._addPeriod(self.start_date, (0, 0, 7))
        self.var_to.set(General.changeDateForamt(self.end_date))
        self._updateChart(self.getTrainings, self.makeChart)

    def _setMonthPeriod (self) -> None:
        """Nastaví měsíční obdodí od počátečního dne při kliknutí na tlačítko měsíc."""
        self.var_from.set(General.changeDateForamt(self.start_date))
        self.end_date = self._addPeriod(self.start_date, (0, 1, 0))
        self.var_to.set(General.changeDateForamt(self.end_date))
        self._updateChart(self.getTrainings, self.makeChart)

    def _setThreeMonthPeriod (self) -> None:
        """Nastaví tříměsíční obdodí od počátečního dne při kliknutí na tlačítko 3 měsíce."""
        self.var_from.set(General.changeDateForamt(self.start_date))
        self.end_date = self._addPeriod(self.start_date, (0, 3, 0))
        self.var_to.set(General.changeDateForamt(self.end_date))
        self._updateChart(self.getTrainings, self.makeChart)

    def _setYearPeriod (self) -> None:
        """Nastaví roční obdodí od počátečního dne při kliknutí na tlačítko rok."""
        self.var_from.set(General.changeDateForamt(self.start_date))
        self.end_date = self._addPeriod(self.start_date, (1, 0, 0))
        self.var_to.set(General.changeDateForamt(self.end_date))
        self._updateChart(self.getTrainings, self.makeChart)

    def _addPeriod (self, original_date : date, delta_time : tuple) -> date:
        """Funkce přičte období k zadanému datu a vrátí výsledné datum.\n
        Vstupy: originální datum, tuple -> (roky, měsíce, dny)."""
        date = original_date + relativedelta(years = delta_time[0], months = delta_time[1], days = delta_time[2])
        return date

    def _updateChart (self, getTrainings, makeChart) -> None:
        """Přegeneruje obsah grufu při inicializace nebo změně nastavení parametrů."""
        chart_legend, chart_counts, chart_colors = getTrainings(self.start_date, self.end_date)
        makeChart(chart_legend, chart_counts, chart_colors)
        self.figure.canvas.draw() # aby se zobrazil aktuální graf
