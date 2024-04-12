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
from icecream import ic
#import souborů
from configuration import unknown_text, unknown_text_label, colors
from ctkWidgets import Label, Button

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
    def checkGreater0(number : float) -> bool:
        """Zjistí, zda je číslo větší než 0. Vrátí bool."""
        if number > 0:
            return True
        return False
    
    def checkFloatEntry (entry : str) -> bool:
        """Ověří, zda je vstupní hodnota float."""
        try:
            float(entry)
            return True
        except:
            return False
    
    @staticmethod
    def checkDateEntry(entry : str, separator = "/") -> bool:
        """Ověří, zda je vstupní hodnota platné datum.
        vstup : dd/mm/yyyy resp. zadaný oddělovač"""
        try:
            date_list = entry.split(separator) # rozdělí vstup
            str_day, str_month, str_year = date_list # uloží list do proměnných
            first = int(str_day) # převede na int
            second = int(str_month)
            third = int(str_year)
            try:
                date(third, second, first) # vytvoří datum
            except:
                date(first, second, third)
            checked = True
        except:
            checked = False
        return checked
    
    @staticmethod
    def dateBetween (date : date, start_border : date, end_border : date) -> bool:
        """Porovná data, pokud je zadané datum mezi hranicemi, vrátí True, jinak False. (porovnání <=)"""
        if start_border <= date <= end_border:
            return True
        return False

    def findSeparator(new_date : str) -> str:
        """Najde oddělovač zadaného data. Pokud se nejedná o žádný z oddělovačů, vrátí None."""
        separators = ["-", "/", ". "]
        for one_sep in separators:
            index = new_date.find(one_sep)
            if index >= 0:
                return one_sep
        return None
    
    @staticmethod
    def stringToDate (date_str : str) -> date:
        """Ze stringu typu pro datum vytvoří datum."""
        sep = General.findSeparator(date_str)
        date_list = date_str.split(sep)
        if len(date_list[0]) > 2:
            new_date = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        else:
            new_date = date(int(date_list[2]), int(date_list[1]), int(date_list[0]))
        return new_date

    @staticmethod
    def changeDateFormat (dt_date : date, separator = ". ") -> str:
        """Změní formát data z formátu date na psaný formát data."""
        return "{1}{0}{2}{0}{3}".format(separator, str(dt_date.day), str(dt_date.month), str(dt_date.year))
    
    @staticmethod
    def prepareString(list :list) -> str:
        """Připraví string jako jeden řádek zápisu do souboru."""
        line = str(list[0])
        if len(line) >= 1:
            for i in range(1, len(list)):
                line = line + " / " + str(list[i])
        return line
    
    @staticmethod
    def preparePersonalDBString (name : str, value : str, date : date) -> str:
        """Připraví řáděk dat pro zapsání informace do databáze osobních údajů uživatele."""
        str_date = General.changeDateFormat(date, "/")
        return "{0}:{1}:{2}".format(name, value, str_date)
    
    @staticmethod
    def emptyToUknowText (data_list : list) -> list:
        """V listu pro zapsání dat do databáze vymění prázné hodnoty (uživatelem nezadané) za hodnoty nezadano."""
        for i in range(len(data_list)):
            if data_list[i] == "":
                data_list[i] = unknown_text
        return data_list
    
    @ staticmethod
    def loadLinesFromFile (file_path : str) -> list:
        """Vrátí list řádků načtených ze zadaného souboru."""
        with open(file_path, 'r') as f:
            lines = f.readlines()
        return lines
    
    @staticmethod
    def appendToFile (path : str, lines : list) -> None:
        """Připíše řádky na konec souboru."""
        with open(path, "a") as f:
            for line in lines:
                f.write(line + "\n")

    @staticmethod
    def overwriteFile (path : str, lines : list) -> None:
        """Vloží zadané řádky do souboru, předchozí obsah vymaže."""
        with open (path, 'w+') as f:
            f.seek(0)
            for line in lines:
                f.write(line)

    @staticmethod
    def setStringForUndefined (message : str, undefined_signs : list) -> list:
        """V tooltip zprávě, vymění hodnoty undefined_signs (list, všech hodnot, které se mají vyměnit), za hodnoty určené k označení nezadaného údaje."""
        for sign in undefined_signs:
            message = message.replace(sign, unknown_text_label)
        return message  

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
    def checkKnownFloat (float_check : str) -> float:
        """Zkontroluje, zda údaj ve tvaru integeru byl vyplněn, pokud ne, uloží do proměnné None."""
        if float_check == unknown_text:
            return None
        return float(float_check)
    
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
    def invertList (data : list) -> list:
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
        """Vrátí datum posunuté od půdního o zadané množství času (dopředu)."""
        start_date = central_date + relativedelta(years = year, months = month, days = day)
        return start_date
    
    @staticmethod
    def surroundingLastDate (start_date : date, 
                              year : int, month : int, day : int) -> date:
        """Vrátí poslední den období zobrazovaného daným sloupcem v grafu."""
        end_date = start_date + relativedelta(years = year, months = month, days = day - 1)
        return end_date
    
    @staticmethod
    def initBackButton (master : object) -> None:
        """Talčítko zpět v nastavování tréninkového plánu."""
        back_button = Button(master, "Zpět", master.master.backToChoiceWindow)
        back_button.grid(row=0, column=0, sticky="NW")
        back_button.configure(width=40)

    @staticmethod
    def setRedBorder (widget : object) -> None:
        """V případě neplatnosti vstupu nastaví okraj widgety na červenou barvu."""
        widget.configure(border_color = colors["dark-red"])

    @staticmethod
    def setDefaultBorder (widget : object) -> None:
        """V případě opravení vstupu nastaví okraj widgety na původní barvu."""
        widget.configure(border_color = colors["entry-border"])

    @staticmethod
    def setWidgetForeColor (widget : object, hex_color : str, hex_hover_color : str) -> None:
        """Nastaví barvu pozadí zadané widgetě (hlavně frame / button)."""
        widget.configure(fg_color = hex_color)
        widget.configure(hover_color = hex_hover_color)

    @staticmethod
    def getBorderTerms (date_list : date) -> date:
        """Z listu seřazených dat formátu date, vrátí 2 data: nejstarší a nejmladší datum."""
        first_date = date_list[0]
        last_date = date_list[-1]
        return first_date, last_date
    
    @staticmethod
    def loadPersonalData (personal_data_path : str) -> dict:
        """Načte osobní údaje o uživateli z databáze osobních údajů. Vrátí slovník údajů zadaných v ruzných datech uživatelem."""
        file_lines = General.loadLinesFromFile(personal_data_path)
        for i in range(len(file_lines)):
            file_lines[i] = file_lines[i].split(":")
        personal_dict = { file_lines[0][0] : file_lines[0][1], }
        for i in range(1, len(file_lines)):
            if file_lines[i][0] in personal_dict.keys():
                personal_dict[file_lines[i][0]].append((file_lines[i][1], file_lines[i][2]))
            else:
                personal_dict[file_lines[i][0]] = [(file_lines[i][1], file_lines[i][2])]
        return personal_dict
