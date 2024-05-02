# import knihoven
from tkinter import *
import customtkinter as ctk
from datetime import date, datetime
from icecream import ic
# import souborů
from dateAndTime import DateAndTime
from general import General
from image import Image as img
from ctkWidgets import Frame, Label, Button
from configuration import colors, trainings_path
import globalVariables as GV


class InfoFrame (Frame):
    """Frame v landing page s doplňkovými informacemi."""
    def __init__ (self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.today_date = date.today()
        self.today_with_time = datetime.now()
        self.dt = DateAndTime(self)
        self.configure(fg_color = "transparent")
        self._lastTrainTime()
        self._initInfoLabels()
        self._initTitle()
        self._updateLastLoginTime()
        self._saveNewLastLogin()

    def _initTitle (self) -> None:
        """Vytvoří obsahové (textové) widgety ve framu."""
        title = Label(self, "Vítej zpět!", ("Calibri", 40, "bold"))
        title.grid(row = 0, column = 0, columnspan = self.columns_number, padx = 10, pady = (10, 40), sticky = "NSWE")
        title.configure(text_color = colors["light"], fg_color = "transparent")

    def _initInfoLabels (self) -> None:
        """Vytvoří labely s informacemi o posledních aktivitách."""
        self.title_font = ("Calibri", 18)
        self.button_size = 90
        self.button_font = ("Poppins", 38, "bold")
        self.label_height = 20
        self.label_font = ("Calibri", 16, "bold")
        self.padx = 6
        self.pady = 3
        self.fg_color = colors["light-gray"]
        self.fg_hover = colors["gray"]
        self._lastLoginWidgets()
        self._lastTrainWidgets()

    def _lastLoginWidgets (self) -> None:
        """Widgety obsahující informace o posledním přihlášení uživatele."""
        periods = self._timeSinceLastLogin()
        self.time_boxes = {
            "count-label" : [],
            "name-label" : [],
            "key" : [],
        }
        self._createLastLoginTimeBoxes(periods)
        abstract = Label(self, "Minulá návštěva před:", self.title_font)
        abstract.grid(row = 1, column = 0, columnspan = self.columns_number, sticky = "NSWE")

    def _createLastLoginTimeBoxes (self, periods : dict) -> None:
        """Vytvoří obdélníkové widgety a labely časových jednotek."""
        i = 0
        for key in periods:
            if periods[key]:
                count = Button(self, periods[key], lambda:  self._buttonFunction())
                count.grid(row = 2, column = i, padx = self.padx, pady = self.pady)
                count.configure(height = self.button_size, width = self.button_size, fg_color = self.fg_color, hover_color = self.fg_hover, font = self.button_font)
                self.time_boxes["count-label"].append(count)
                name = Label(self, self.dt.periodInflection(periods[key], key), self.label_font)
                name.grid(row = 3, column = i, padx = self.padx, pady = self.pady)
                name.configure(width = self.button_size, height = self.label_height, fg_color = "transparent")
                self.time_boxes["name-label"].append(name)
                self.time_boxes["key"].append(key)
                i = i + 1
        self.columns_number = i

    def _lastTrainWidgets (self) -> None:
        """Widgety obsahující informace o posledním zadaném tréninku."""
        abstract = Label(self, "Poslední trénink před:", self.title_font)
        abstract.grid(row = 4, column = 0, columnspan = self.columns_number, sticky = "NWSE", pady = (20, 0))
        day_number = self._timeSinceLastTrain()
        count = Button(self, day_number, lambda: self._buttonFunction())
        count.grid(row = 5, column = 0, columnspan = self.columns_number, padx = self.padx, pady = self.pady)
        count.configure(height = self.button_size, width = self.button_size, fg_color = self.fg_color, hover_color = self.fg_hover, font = self.button_font)
        name = Label(self, self.dt.periodInflection(day_number, "day"), self.label_font)
        name.grid(row = 6, column = 0, columnspan = 5, padx = self.padx, pady = self.pady)
        name.configure(width = self.button_size, height = self.label_height, fg_color = "transparent")

    def _buttonFunction (self) -> None:
        """Funkce buttonu..."""
        ...
        return None

    def _lastTrainTime (self) -> None:
        """Vypočítá doba od zadání posledního tréninku a nastaví ji."""
        dates = self._loadTrainDates()
        dates.sort()
        self.last_train = dates[-1]

    def _loadTrainDates (self) -> None:
        """Z databáze tréninků načte list dat složený z data konaní každého tréninku."""
        lines = General.loadLinesFromFile(trainings_path)
        dates = [None] * len(lines)
        for i in range(len(lines)):
            lines[i] = General.separateData(lines[i])
            separator = General.findSeparator(lines[i][0])
            list = lines[i][0].split(separator)
            dates[i] = "20{0}/{1}/{2}".format(list[2], list[1], list[0])
            dates[i] = General.stringToDate(dates[i])
        return dates
    
    def _timeSinceLastTrain (self) -> int:
        """Spočítá dobu od posledního tréninku a vrátí ji jako string."""
        difference = (self.today_date - self.last_train).days
        return difference
    
    def _timeSinceLastLogin (self) -> str:
        """Spočítá dobu od posledního přihlášení do aplikace a vrátí ji jako string."""
        self.last_login = datetime.strptime(GV.last_login, '%Y-%m-%d %H-%M-%S')
        dt = DateAndTime(self)
        periods = dt.getDuration(self.last_login, datetime.now())
        return periods
    
    def _saveNewLastLogin (self) -> None:
        """Uloží do setting database nový čas posledního přihlášení."""
        GV.setting["last-login"] = self.today_with_time.strftime("%Y-%m-%d %H-%M-%S")
        GV.overwriteSettingFile()

    def _updateLastLoginTime (self) -> None:
        """Aktualizuje text v labelu s časem od posledního přihlášení.\n
        Spustí se každou vteřinu."""
        periods = self._timeSinceLastLogin()
        new_timebox = self._createNewTimeBoxCheck(periods)
        if not new_timebox:
            for i in range(len(self.time_boxes["key"])):
                key = self.time_boxes["key"][i]
                time_period_name = self.dt.periodInflection(periods[key], key)
                self.time_boxes["count-label"][i].configure(text = periods[key])
                self.time_boxes["name-label"][i].configure(text = time_period_name)
        else:
            # self._createLastLoginTimeBoxes(periods)
            General.deleteFrameWidgets(self)
            self._initInfoLabels()
            self._initTitle()
        # znovuzavolání funkce
        self.after(1000, self._updateLastLoginTime)

    def _createNewTimeBoxCheck (self, periods : dict) -> bool:
        """Zkontroluje, zda je třeba přidat nový timebox nebo se jen přičte číslo do stavajících.\n (pokud je čas 0:0:59 s -> musí se přidat políčko minuta -> fce vrátí true... jinak False.)"""
        for key in periods:
            if not periods[key]: continue
            if not key in self.time_boxes["key"]:
                return True
        return False