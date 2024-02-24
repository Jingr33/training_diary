# import knihoven
from datetime import date
from dateutil.relativedelta import *
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,) # pro přenesení matplotlibu do tkintru
from tkinter import * 
import customtkinter as ctk
from numpy import transpose
#import souborů
from configuration import unknown_text
from ctkWidgets import Label

class General():
    """Třídá základních statických funkcí používaných na hodně místech."""
    @staticmethod
    def checkIntEntry(entry: str) -> bool:
        """Ověří zda je vstupní hodnota int."""
        try:
            int(entry)
            checked = True
        except:
            checked = False
        return checked
    
    @staticmethod
    def checkDateEntry(entry : str, separator = "/") -> bool:
        """Ověří, zda je vstupní hodnota platné datum.
        vstup : dd/mm/yyyy"""
        try:
            date_list = entry.split("/") # rozdělí vstup
            str_day, str_month, str_year = date_list # uloží list do proměnných
            day = int(str_day) # převede na int
            month = int(str_month)
            year = int(str_year)
            entry_date = date(year, month, day) # vytvoří datum
            checked = True
        except:
            checked = False
        return checked
        
    def findSeparator(new_date : str) -> str:
        """Najde oddělovač zadaného data. Pokud se nejedná o žádný z oddělovačů, vrátí None."""
        separators = ["-", "/", ". "]
        for one_sep in separators:
            index = new_date.find(one_sep)
            if index >= 0:
                return one_sep
        return None
    
    @staticmethod
    def changeDateForamt (dt_date : date) -> str:
        """Změní formát data z formátu date na psaný formát data."""
        return str(dt_date.day) + ". " + str(dt_date.month) + ". " + str(dt_date.year)
    
    @staticmethod
    def prepareString(list :list) -> str:
        """Připraví string jako jeden řádek zápisu do souboru."""
        line = str(list[0])
        if len(line) >= 1:
            for i in range(1, len(list)):
                line = line + " / " + str(list[i])
        return line
    
    @ staticmethod
    def loadLinesFromFile (file_path : str) -> list:
        """Vrátí list řádků načtených ze zadaného souboru."""
        with open(file_path, 'r') as f:
            lines = f.readlines()
        return lines      

    @staticmethod
    def isFileEmpty (file_path) -> bool:
        """Zjistí, zda je soubor prázdný, či ne, vrátí boolean."""
        return os.stat(file_path).st_size == 0
    
    @staticmethod
    def separateData (one_line : str) -> list:
        """Přijme řádek data načtených ze souboru. Vrátí list oddělených údajů."""
        return one_line.split(" / ")
    
    @staticmethod
    def checkIfSet (string : str) -> str:
        """Zkontroluje, zda je údaj zadaný, pokud ano, vrátí ho, pokud ne, vrátí do něj None."""
        if string:
            return string
        else:
            return None
        
    @staticmethod 
    def checkKnownInt (integer_check : str) -> float:
        """Zkontroluje, zda údaj ve tvaru integeru byl, pokud ne, uloží do proměnné None."""
        if integer_check == unknown_text:
            return None
        return float(integer_check)
    
    @staticmethod
    def deleteFrameWidgets (widget_parent : object) -> None:
        """Vymaže widgety ze zadaného framu."""
        for widget in widget_parent.winfo_children():
            widget.destroy()

    @staticmethod
    def deleteListWidgets (widgets : list) -> list:
        """Vymaže widgety ze zadaného listu. Vrátí prázdný list"""
        for widget in widgets:
            widget.destroy()
        return []
    
    @staticmethod
    def pasteChart(master : object, grid : (tuple), columnspan : int) -> None:
        """Vytvoří widgetu s matplotlib grafem.\n
        master - objekt\n
        grid - tuple (sloupec, řádek).\n
        colulmnspan - int"""
        # vytvoření figure
        width = 100
        height = 5
        # nastavení designu
        plt.style.use('dark_background')
        # figure
        master.figure = Figure(figsize=(width, height), dpi=(100))
        master.figure.tight_layout()
        # převedení do tkinteru
        figure_canvas = FigureCanvasTkAgg(master.figure, master)
        figure_canvas.draw()
        #vytvoření matplotlibu v tkinteru
        widget = figure_canvas.get_tk_widget()
        widget.grid(column = grid[0], row = grid[1], columnspan=columnspan, padx = 12, pady = 5)

    @staticmethod
    def _invertList (data : list) -> list:
        """Vrátí 2d list transponovaně."""
        return transpose(data)
    
    @staticmethod
    def renderErrorToChart (master : object, text : str, grid : tuple) -> None:
        """Vytvoří label s erorovým nápisem na místo vykreslení grafu v případě, že data zaslaná 
        do grafu jsou prázdná."""
        master.error_l = Label(master, text, ("Arial", 13, "bold"))
        master.error_l.grid(row = grid[0], column = grid[1], columnspan = 4,
                             padx = 5, pady = 5, sticky = "NSEW")

    @staticmethod    
    def surroundingFirstDate (central_date : date, 
                               year : int, month : int, day : int) -> date:
        """Vrátí první den období zobrazovaného daným sloupcem v grafu."""
        start_date = central_date + relativedelta(years = year, months = month, days = day)
        return start_date
    
    @staticmethod
    def surroundingLastDate (start_date : date, 
                              year : int, month : int, day : int) -> date:
        """Vrátí poslední den období zobrazovaného daným sloupcem v grafu."""
        end_date = start_date + relativedelta(years = year, months = month, days = day - 1)
        return end_date
