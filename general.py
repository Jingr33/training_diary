# import knihoven
from datetime import date
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,) # pro přenesení matplotlibu do tkintru
from tkinter import * 
import customtkinter as ctk
from math import floor
#import souborů
from configuration import unknown_text

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
    def checkDateEntry(entry : str) -> bool:
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
    
    # @staticmethod
    # def lenghtOfPeriod (start : date, end : date) -> int:
    #     """Metoda vrátí počet dní mezi počátečním a koncovým datem."""
    #     ...

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
        master.figure = Figure(figsize=(width, height), dpi=(100))
        # převedení do tkinteru
        figure_canvas = FigureCanvasTkAgg(master.figure, master)
        figure_canvas.draw()
        # vytvoření subplotu
        master.dots = master.figure.add_subplot()
        #vytvoření matplotlibu v tkinteru
        widget = figure_canvas.get_tk_widget()
        widget.grid(column = grid[0], row = grid[1], columnspan=columnspan, padx = 12, pady = 5)

