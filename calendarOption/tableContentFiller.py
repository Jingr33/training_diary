#import knihoven
import calendar
from tkinter import *
import customtkinter as ctk
from configuration import trainings_path
from datetime import date
# importy osuborů
from oneTraining import OneTraining

class TabelContentFiller ():
    """Třída pro plnění kalendáře daty pro zvolený měsíc."""
    def __init__(self, date : tuple):
        self.date = date
        # první a poslední den zobrazený v aktuálním kalendáři
        self.first_date = self._firstDate()
        self.last_date = self._lastDate()
        # list s kalendářními daty pro jednotlivé framy
        self.dates_list = self._datesDayList()

        # test
        self.trainings = self._loadTrainingns()

    def datesToLabelsConfig(self, frame_list : list, date_list : list) -> None:
        """Metoda pro přidání textu s datem do každého labelu -> framu kalendáře."""
        # cyklus přes framy
        for i in range(len(frame_list)):
            frame_list[i].label.configure(text = date_list[i])

    def displayTrainingWidget(self, frame_list : tuple) -> None:
        """Metoda pro zobrazení widgety s tréninkem v daném dni v kalendáři."""
        # vymazaní předchozího obsahu v kalendáři
        for frame in frame_list:
            for strip in frame.strips:
                strip.destroy()
        # vykreslení stripů s tréninky v jednotlivých dnech
        for training in self.trainings:
            index_of_frame = self._frameIndexOfDay(training.real_date)
            frame_list[index_of_frame].createStrip(training)

    
    def _datesDayList (self) -> list:
        """Metoda vrátí list dat pro každý den (čtvereček) z kalendáře."""
        # tuple s hodnotou prvního dne v týdnu zadaného měsíce
        # a hodnotou počtu dní v měsíci
        key_dates = self._firstDay_NumOfDays(self.date)
        # získání pčtu dní předchozího měsíce
        prev_month_date = self._prevMonth(self.date)
        # tuple s key_dates predchozího měsíce
        prev_month_key_dates = self._firstDay_NumOfDays(prev_month_date)
        next_month_date = self._nextMonth(self.date)

        # deklarace listu pro hodnoty dat
        dates_list = [None] * 42
        # naplnění listu daty aktuálního měsíce 
        # (od hodnoty dne kterým měsíc začíná -> počet dní krát)
        date_increment = 1
        for i in range(key_dates[0], key_dates[1] + key_dates[0]):
            dates_list[i] = str(date_increment)
            date_increment = date_increment + 1
        # naplnění hodnotami po skončení měsíce
        date_increment = 1
        for j in range(key_dates[0] + key_dates[1], 42):
            string = str(date_increment) + ". " + str(next_month_date[1]) + "."
            dates_list[j] = string
            date_increment = date_increment + 1
        # naplnění daty před začátkem zvoleného měsíce
        date_increment = prev_month_key_dates[1] - key_dates[0] # poč. dní předch. měsíce - den začátku tohoto měsíce
        for k in range(0, key_dates[0]):
            string = str(date_increment) + ". " + str(prev_month_date[1]) + "."
            dates_list[k] = date_increment
            date_increment = date_increment + 1
        return dates_list

    def _firstDay_NumOfDays (self, date : tuple) -> int:
        "Funkce zjistí, jaký den v týdnu je 1. v měsíci a kolik má měsíc dní."
        return calendar.monthrange(date[0], date[1])


    def _prevMonth (self, date : tuple) -> list:
        """Posune nastavený měsíc o jeden zpět."""
        month = date[1]
        year = date[0]
        if month >= 2:
            month = month - 1
        else:
            month = 12
            year = year - 1
        date = (year, month)
        return date
    
    def _nextMonth (self, date : tuple) -> list:
        """Posune nastavený měsíc o jeden dopředu."""
        month = date[1]
        year = date[0]
        if month <= 11:
            month = month + 1
        else:
            month = 1
            year = year + 1
        date = (year, month)
        return date
    
    def _loadTrainingns(self) -> list:
        """Metoda pro načtení tréninků pomocí OneTraining z databáze.
        Vrátí list tréninků"""
        # načtení všech dat do pole po jednotlivých řádcích
        with open(trainings_path, 'r') as f:
            lines = f.readlines()
        
        # vytvoření objektů jednotlivých tréninků
        trainings = []
        for one_line in lines:
            one_training = OneTraining(self, "load", one_line)
            # vyhodnocení, zda trénink je v tomto kalendáři vidět
            between = one_training.trainingDateBetween(self.first_date, self.last_date)
            if between:
                trainings.append(one_training)
        return trainings
        
    def _frameIndexOfDay (self, date_of_training : date) -> int:
        """Metoda vrátí index framu se dnem, do kterého se má widgeta zobrazit."""
        training_date = (date_of_training.year, date_of_training.month)
        prev_month_date = self._prevMonth(self.date) # data předchozího měsíce
        next_month_date = self._nextMonth(self.date) # data přístího měsíce
        key_dates = self._firstDay_NumOfDays(self.date) # klíčové údaje o zvoleném měsíci
        # pokud je trénink v měsíci který odpovídá vybranému měsíci
        if training_date == self.date:
            frame_index = key_dates[0] + date_of_training.day - 1
        # pokud je trénink v předchozím měsíci, al eve viditelné oblasti
        elif training_date == prev_month_date:
            first_date = self._firstDate(self.date)  # první den zobrazený v kalendáři
            frame_index = key_dates[1] - first_date.day - 1
        # pokud je trénink v následujícím měsíci, ale ve viditelné oblasti
        elif training_date == next_month_date:
            frame_index = key_dates[0] + key_dates[1] + date_of_training.day - 1
        return frame_index

    def _firstDate (self) -> date:
        """Vrátí datum prvního dne zobrazovaného v tabulce."""
        # získání dat
        key_dates = self._firstDay_NumOfDays(self.date)
        prev_month_date = self._prevMonth(self.date)
        prev_key_dates = self._firstDay_NumOfDays(prev_month_date)
        # datum prvního dne v kalendáři
        if key_dates[0] == 0:
            first_date = date(self.date[0], self.date[1], 1)
        else:
            day = prev_key_dates[1] + 1 - key_dates[0]
            first_date = date(prev_month_date[0], prev_month_date[1], day)
        return first_date
    
    def _lastDate (self) -> date:
        """Vrátí datum posledního dne zobrazeného v kalendáří."""
        # získání dat
        key_dates = self._firstDay_NumOfDays(self.date)
        next_month_date = self._nextMonth(self.date)
        # datum posledního dne v kalendáři
        day = 42 - key_dates[0] - key_dates[1]
        last_date = date(next_month_date[0], next_month_date[1], day)
        return last_date
    
    # máš vybrané tréninky, které je třeba vykreslit v kalendáři
    #TODO - přiřaď widgety na správné místa v kalendáři
            # zobraz je a smaž předchozí widgety (to asi bude oříšek)
            # kdyžtak předělej načítání dat, ať se nenačítají všechny tréninky ale jen ty co jsou potřeba