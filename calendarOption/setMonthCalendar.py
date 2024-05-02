# importy knihoven
from tkinter import *
import customtkinter as ctk
from datetime import datetime
# importy souborů
from ctkWidgets import Frame, Button, Label
from configuration import months

class SetMonth (Frame):
    "Frame (horní) pro nastavování období (měsíce) zobrazovaném v kalendáři."
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        # zjištění aktuálního data
        self.setted_date = self._currentMonth()
        # vyvolání grafického rozhraní
        self._initSliderGUI()

    def _initSliderGUI(self) -> None:
        """Metoda pro vytvoření grafického rozhraní překlikávání měsíců v kalendáři."""
        # nastavení aktuálního měsíce do labelu
        self.var_text = self._formatMonth(self.setted_date)
        # button pro překliknutí na dřívější měsíc
        self.prev_b = Button(self, "Předchozí", self._prevMonth)
        self.prev_b.pack(side=LEFT, anchor = ctk.E, pady = 15)
        self.prev_b.configure(width=40)
        # label aktuálního měsíce
        self.now_l = Label(self, self.var_text, ("Arial", 15, "bold"))
        self.now_l.pack(side=LEFT, anchor = ctk.CENTER, pady = 15, padx = 10)
        self.now_l.configure(width = 120)
        # button pro překliknutí na následující měsíc
        self.next_b = Button(self, "Následující", self._nextMonth)
        self.next_b.pack(side=LEFT, anchor = ctk.W, pady = 15)
        self.next_b.configure(width=40)

    def _currentMonth (self) -> tuple:
        """Vytvoří tuple (rok, měsíc) aktuálního měsíce."""
        current_date = (datetime.now().year, datetime.now().month)
        return current_date
    
    def _formatMonth (self, date :tuple) -> str:
        """Vytvoří string pro vypsání v labelu."""
        current_month = str(months[date[1]])
        current_year = str(date[0])
        string = current_month + " " + current_year
        return string
    
    def _prevMonth (self) -> None:
        """Posune nastavený měsíc o jeden zpět."""
        month = self.setted_date[1]
        year = self.setted_date[0]
        if month >= 2:
            month = month - 1
        else:
            month = 12
            year = year - 1
        self.setted_date = (year, month)
        self.var_text = self._formatMonth(self.setted_date)
        self.now_l.configure(text =self.var_text)

    def _nextMonth (self) -> None:
        """Posune nastavený měsíc o jeden dopředu."""
        month = self.setted_date[1]
        year = self.setted_date[0]
        if month <= 11:
            month = month + 1
        else:
            month = 1
            year = year + 1
        self.setted_date = (year, month)
        self.var_text = self._formatMonth(self.setted_date)
        self.now_l.configure(text = self.var_text)