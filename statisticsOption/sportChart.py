# import knihoven
from tkinter import * 
import customtkinter as ctk
import matplotlib.pyplot as plt
from datetime import date
from dateutil.relativedelta import *
from numpy import transpose, arange
# import souborů
from statisticsOption.dataLoader import DataLoader
from sports.setSport import SetSport
from general import General
from ctkWidgets import Frame, Label, ComboBox, Button, Entry
from configuration import chart_range_option, chart_frame_color, sport_list

class SportChart (Frame):
    """Frame s grafem ukazující poměr vykonaných sportů."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.columnconfigure([0,1,2,3,4], weight=1)
        self.time_range_func = [self._dailyColumn, self._weeklyColumn, self._monthlyColumn, self._yearlyColumn]
        self.today = date.today()
        self.actual_date = self.today
        self.configure(corner_radius = 10, fg_color = chart_frame_color)
        self._initGUI()


        # , bbox_inches='tight' 

    def _initGUI(self) -> None:
        """Vytvoření grafického rozhraní."""
        self._initWidgets()
        General.pasteChart(self, (0, 1), 5)

    def _initWidgets (self) -> None:
        """Vytvoří widgety nad grafem sportů."""
        name = Label(self, "Sporty", ("Arial", 20, "bold"))
        name.grid(column = 0, row = 0, padx = 5, pady = 15)

        range_l = Label(self, "Období:")
        range_l.grid(column = 3, row = 0, sticky=ctk.E, padx = 5)

        self.var_option = StringVar()
        self.range_cb = ComboBox(self, chart_range_option, self._updateChart, self.var_option)
        self.range_cb.grid(column = 4, row = 0)
        self.range_cb.configure(width = 100)
        self.var_option.set(chart_range_option[1])
        self.range = chart_range_option[1]
        
        self._initSetTime()

    def _initSetTime (self) -> None:
        """Vytvoří widgety pro nastavování zobrazovaného období."""
        prev_button = Button(self, "<", ...)
        prev_button.grid(column = 1, row = 2, sticky = ctk.E)
        prev_button.configure(corner_radius = 6, height= 30, width=30)

        self.var_central_date = ctk.StringVar()
        central_date = Entry(self, self.var_central_date)
        central_date.grid(column = 2, row = 2, padx = 6, pady = 5)
        central_date.configure(width = 75)
        self.var_central_date.set(self.today)
        # event pro přegenerování grafu při přepsání data
        central_date.bind("<FocusOut>", self._updateChart)

        next_button = Button(self, ">", ...)
        next_button.grid(column = 3, row = 2, sticky = ctk.W)
        next_button.configure(corner_radius = 6, height= 30, width=30)

    def _updateChart (self, value) -> None:
        """Updatuje graf při jakékoliv změně nastavení ve framu."""
        border_dates = self._setTimeRange(value)
        trainings = self._getTrainingsInPeriod(border_dates)
        chart_data = self._numberOfTrainings(trainings)
        self._makeChart(chart_data)


    def _setTimeRange(self, value) -> None:
        """Nastaví období zobrazované jedním sloupcem v grafu. Vrátí list hraničních dat 
        pro každý sloupec grafu."""
        self.range = value
        self.var_central_date.set(self.today)
        self.actual_date = self.today
        border_dates = self._setDateBorders(value)
        return border_dates
        
    def _setDateBorders (self, value) -> None:
        """Nastaví hraniční data časových úseků, pro které se zobrazuje jeden sloupec v grafu."""
        index = chart_range_option.index(value)
        dates = self.time_range_func[index]() # počateční a koncová data jednotlivých sloupců grafu
        return dates

    def _dailyColumn (self) -> list:
        """Rozdělí časové úseky po dni a vrátí list tuplů a počátečním a koncovým dnem
        časového úseku."""
        central_date = self.actual_date
        periods = [None] * 7
        for i in range(-3, 4):
            start_date = self._surroundingFirstDate(central_date, 0, 0, i)
            end_date = start_date
            periods[i + 3] = (start_date, end_date)
        return periods
    
    def _weeklyColumn (self) -> None:
        ...

    def _monthlyColumn (self) -> None:
        ...
    
    def _yearlyColumn (self) -> None:
        ...

    def _surroundingFirstDate (self, central_date : date, 
                               year : int, month : int, day : int) -> date:
        """Vrátí první den období zobrazovaného v některém z okolních sloupců."""
        start_date = central_date + relativedelta(years = year, months = month, days = day)
        return start_date

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

    def _periodNumbers (self, period : list) -> list:
        """Spočítá, kolik tréninků v zadaném listu náleželo jednotlivým sportům.
        Vrátí list s počty tréninků."""
        train_numbers = [0] * len(sport_list)
        for training in period:
            for i in range(len(sport_list)):
               if training.sport == sport_list[i]:
                   train_numbers[i] = train_numbers[i] + 1
                   break
        return train_numbers
    
    def _makeChart (self, data : list) -> None:
        """Vytvoří nový obsah grafu."""
        num_of_columns = 7
        ind = arange(num_of_columns)
        transp_data = self._invertList(data)
        width = 0.35
        for i in range(len(data[0])):
            plot = plt.bar(ind, transp_data[i], width, bottom=transp_data[0])
        plt.show()

    def _invertList (self, data : list) -> list:
        """Vrátí 2d list transponovaně."""
        return transpose(data)