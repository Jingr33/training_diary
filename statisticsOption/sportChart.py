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
from configuration import chart_range_option, chart_frame_color, sport_list, sport_color

class SportChart (Frame):
    """Frame s grafem ukazující poměr vykonaných sportů."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.columnconfigure([0,1,2,3,4], weight=1)
        self.time_range_func = [self._dailyColumn, self._weeklyColumn, self._monthlyColumn, self._yearlyColumn]
        self.today = date.today()
        self.actual_date = self.today
        self.figure = None
        self.chart = None # proměnná pro graf
        self.xdata = None # popisky osy x (data)
        self.configure(corner_radius = 10, fg_color = chart_frame_color)
        self._initGUI()
        self.range = self.var_option.get()
        self._updateChart(self.range)
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
        prev_button = Button(self, "<", self._prevPeriod)
        prev_button.grid(column = 1, row = 2, sticky = ctk.E)
        prev_button.configure(corner_radius = 6, height= 30, width=30)

        self.var_central_date = ctk.StringVar()
        central_date = Entry(self, self.var_central_date)
        central_date.grid(column = 2, row = 2, padx = 6, pady = 5)
        central_date.configure(width = 85)
        self.var_central_date.set(General.changeDateForamt(self.today))
        # event pro přegenerování grafu při přepsání data v entry
        central_date.bind("<FocusOut>", self._newDateInEntry)
        central_date.bind("<Return>", self._newDateInEntry)

        next_button = Button(self, ">", self._nextPeriod)
        next_button.grid(column = 3, row = 2, sticky = ctk.W)
        next_button.configure(corner_radius = 6, height= 30, width=30)

    def _updateChart (self, value) -> None:
        """Updatuje graf při jakékoliv změně nastavení ve framu."""
        self.border_dates = self._setTimeRange(value)
        trainings = self._getTrainingsInPeriod(self.border_dates)
        chart_data = self._numberOfTrainings(trainings)
        self._makeChart(chart_data)
        self.figure.canvas.draw() # aby se zobrazil aktuální graf

    def _setTimeRange(self, value) -> None:
        """Nastaví období zobrazované jedním sloupcem v grafu. Vrátí list hraničních dat 
        pro každý sloupec grafu."""
        self.range = value
        self.var_central_date.set(General.changeDateForamt(self.actual_date))
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
        periods = self._setColumnDates(0, 0, 1)
        xdata = self._firstDatesList(periods)
        self._chartXData(xdata, True, True)
        return periods
    
    def _weeklyColumn (self) -> None:
        periods = self._setColumnDates(0, 0, 7)
        xdata = self._firstDatesList(periods)
        self._chartXData(xdata, True, True)
        return periods

    def _monthlyColumn (self) -> None:
        periods = self._setColumnDates(0, 1, 0)
        xdata = self._firstDatesList(periods)
        self._chartXData(xdata, True, False)
        return periods
    
    def _yearlyColumn (self) -> None:
        periods = self._setColumnDates(1, 0, 0)
        xdata = self._firstDatesList(periods)
        self._chartXData(xdata, False, False)
        return periods

    def _setColumnDates(self, year : int, month : int, day : int) -> list:
        """Vytvoří list dat složený z tuplů obsahujících počáteční a koncová data každého 
        sloupce v grafu. Vstupy jsou 0 nebo 1int, podle toho, o kterou hodnotu (a kolik) se mají jednotlivé sloupce lišit."""
        central_date = self.actual_date
        periods = [None] * 7
        for i in range(-3, 4):
            start_date = self._surroundingFirstDate(central_date, i*year, i*month, i*day)
            end_date = self._surroundingLastDate(start_date, year, month, day)
            periods[i + 3] = (start_date, end_date)
        return periods
    
    def _firstDatesList (self, periods : list) -> list:
        """Ze vstupního listu tuplů počátečních a koncových dat časovéhoúseku zobrazovaného
          sloupcem vytvoří list počátečních dat sloupců pro popis osy x v grafu."""
        xdata = [None] * len(periods)
        for i in range(len(periods)):
            xdata[i] = periods[i][0]
        return xdata

    def _surroundingFirstDate (self, central_date : date, 
                               year : int, month : int, day : int) -> date:
        """Vrátí první den období zobrazovaného daným sloupcem v grafu."""
        start_date = central_date + relativedelta(years = year, months = month, days = day)
        return start_date
    
    def _surroundingLastDate (self, start_date : date, 
                              year : int, month : int, day : int) -> date:
        """Vrátí poslední den období zobrazovaného daným sloupcem v grafu."""
        end_date = start_date + relativedelta(years = year, months = month, days = day - 1)
        return end_date

    def _chartXData(self, xdata : list, months : bool, days : bool) -> None:
        """Nastaví vlastnost xdata (labely jednotlivých sloupců v grafu na x-ové ose.) tak,
        aby vizuálně odpovídaly zvolenému období."""
        for i in range(len(xdata)):
            chart_date = str(xdata[i].year)
            if months:
                chart_date = str(xdata[i].month) + "/" + chart_date
            if days:
                chart_date = str(xdata[i].day) + "/" + chart_date
            xdata[i] = chart_date
        self.xdata = xdata

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
        # vytvoření subplotu
        self.figure.clf()
        self.chart = self.figure.add_subplot(111)
        # vykreslení grafu
        num_of_columns = 7
        ind = arange(num_of_columns)
        transp_data = self._invertList(data)
        width = 0.6
        for i in range(len(data[0])):
            if i == 0:
                bar_plot = self.chart.bar(ind, transp_data[i], width, color = sport_color[sport_list[i]])
            else:
                bar_plot = self.chart.bar(ind, transp_data[i], width, bottom = transp_data[0], color = sport_color[sport_list[i]])
            self._barLabel(bar_plot, transp_data[i])
        self._chartLabels()

    def _barLabel (self, plot : object, data : list) -> None:
        """Přidá každému sloupci v grafu popisek s číslem jeho četnosti."""
        self.chart.bar_label(plot, label_type='center', fmt = lambda label: self._barLabelFormat(label))

    def _barLabelFormat (self, label : str) -> str:
        """Naformátuje label sloupce -> pokud je nula nevypíše ho."""
        if label:
            return int(label)
        return ""

    def _chartLabels (self) -> None:
        """Nastaví popisky grafu."""
        self.chart.legend(sport_list)
        self.chart.set_xlabel("Datum")
        self.chart.set_ylabel("Počet tréninků")
        self.chart.set_title("Počet typů tréninků za období")
        self.chart.set_xticks(range(len(self.xdata)))
        self.chart.set_xticklabels(self.xdata, rotation='horizontal', fontsize = 8)

    def _invertList (self, data : list) -> list:
        """Vrátí 2d list transponovaně."""
        return transpose(data)
    
    def _prevPeriod (self) -> None:
        """Po stusknutí tlačítka "<" se nastaví datum středového sloupce na o jeden dřívější 
        cyklus a celý graf se posune o cyklus do minulosti."""
        self.actual_date = self.border_dates[2][0]
        self.var_central_date.set(General.changeDateForamt(self.actual_date))
        self._updateChart(self.range)

    def _nextPeriod (self) -> None:
        """Po stusknutí tlačítka ">" se nastaví datum středového sloupce na o jeden pozdější
        cyklus a celý graf se posune o cyklus do budoucnosti."""
        self.actual_date = self.border_dates[4][0]
        self.var_central_date.set(General.changeDateForamt(self.actual_date))
        self._updateChart(self.range)

    def _newDateInEntry(self, value) -> None:
        """Funkce zkontroluje datum zapsané uživatelem do entry pod grafem.
        Pokud je vpořádku, aktualizuje graf s tímto datem, pokud ne, vrátí původní."""
        new_date = self.var_central_date.get()
        date_check = self._checkNewDate(new_date) # kontrola data
        if date_check:
            self.var_central_date.set(General.changeDateForamt(self.actual_date))
        self._updateChart(self.range)

    def _checkNewDate (self, new_date : str) -> bool:
        """Zkontroluje, zda se jedná o datum. Vrátí T/F. Pokud True -> nastaví datum jako actual_date."""
        date_check = True
        try:
            separator = self._findSeparator(new_date)
            if separator:
                date_list = new_date.split(separator)
                dt_date = date(int(date_list[2]), int(date_list[1]), int(date_list[0]))
                self.actual_date = dt_date
            else:
                date_check = False
        except:
            date_check = False
        return date_check
    
    def _findSeparator(self, new_date : str) -> str:
        """Najde oddělovač zadaného data. Pokud se nejedná o žádný z oddělovačů, vrátí None."""
        separators = ["-", "/", ". "]
        for one_sep in separators:
            index = new_date.find(one_sep)
            if index >= 0:
                return one_sep
        return None
    