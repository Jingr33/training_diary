#import knihoven
import calendar
from tkinter import *
import customtkinter as ctk

class TabelContentFiller ():
    """Třída pro plnění kalendáře daty pro zvolený měsíc."""
    def __init__(self, date : tuple):
        self.date = date
        # list s kalendářními daty pro jednotlivé framy
        self.dates_list = self._datesDayList()

    def DatesToLabelsConfig(self, frame_list : list, date_list : list) -> None:
        """Metoda pro přidání textu s datem do každého labelu -> framu kalendáře."""
        # cyklus přes framy
        for i in range(len(frame_list)):
            frame_list[i].label.configure(text = date_list[i])
    
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
        for i in range(key_dates[0] ,key_dates[1] + key_dates[0]):
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

    def _frameIndexOfDay (self) -> int:
        """Metoda vrátí index framu se dnem, do kterého se má widgeta zobrazit."""
        ...
