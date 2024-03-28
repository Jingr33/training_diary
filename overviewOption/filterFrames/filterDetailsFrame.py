#import knihoven
import customtkinter as ctk
from tkinter import *
from math import floor
from icecream import ic
#import souborů
from ctkWidgets import Frame, Label, Button, Entry
from configuration import gym_body_parts, sport_list, colors


class FilterDetails (Frame):
    """Frame pro filtrování detailnějšího nastavení podle zvoleného sportu."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        # nastavení pole plného jedniček "selected" o rozsahu všech sportů
        all_selected = [None] * len(sport_list)
        for i in range(len(all_selected)):
            all_selected[i] = 1
        # vytvoření grafického rozhraní nastavéní filtrů
        self.createAllGUI(all_selected)

    def createAllGUI(self, selected_sports):
        """Vyrenderuje detailní nastavení sportů podle toho, které jsou vybrané."""
        # proměnná, která říká, na kolikátý řádek se má vygenerovat nové nastavení
        self.details_rows = 0
        # pole funkcí generující podrobné nastavení jednotlivých sportu
        self.gui_functions = [self._createGym, self._createRun, self._createSwim]
        # cyklus přes všechny sporty, které se dají vyselectovat
        for i in range(len(selected_sports)):
            if int(selected_sports[i]) == 1: 
                # pokud je sport vybraný spustí se funkce generování jeho podrobného nastavení
                self.gui_functions[i]()

    def filtered(self):
        """Vrátí hodnoty zvolené ve filtru detailů sportů."""
        gym_values = self._filteredGym()
        run_values = self._filteredRun()
        swim_values = self._filteredSwim()
        self.details_widgets = [self.gym_details_widgets, self.run_details_widgets, self.swim_details_widgets]
        filtered = [gym_values, run_values, swim_values]
        return filtered

    def _createGym(self) -> None:
        """Metoda pro vytvoření grafiky pro filtraci jednotlivých části těla."""
        self.gym_rows = 2
        # inicializace grafiky
        self.label = Label(self, "Části těla: ", font=("Arial", 10))
        self.label.grid(row = self.details_rows, column=0)
        self.label.configure(width = 30)
        self.gym_details_widgets = [self.label] + [None] * len(gym_body_parts)
        # přepínače částí těla
        for i in range(len(gym_body_parts)):
            self._createBodyPartSwitchers(i)
        #pole jedniček pro přidávání  zvolených částí těla při filtrování
        self.selected_buttons = [1] * len(gym_body_parts)
        # zvýšení řádku pro následné generování dalšího nastavení
        self.details_rows = self.details_rows + self.gym_rows

    def _createBodyPartSwitchers (self, i : int) -> None:
        """Vygeneruje přepínací tlačítka udávající, které části těla se vyfiltrují a které ne."""
        self.button_switcher = Button(self, gym_body_parts[i], lambda: self._clickedButton(i))
        row, column = self._switcherGridCoord(i)
        self.button_switcher.grid(row = row, column = column, padx = 1, pady = 0, ipadx = 0, ipady = 0)
        self.button_switcher.configure(font = ("Arial", 10), height = 15, width = 20, anchor = ctk.W, fg_color = colors["dodger-blue-4"])
        self.gym_details_widgets[i + 1] = self.button_switcher

    def _switcherGridCoord (self, index : int) -> int:
        """podle pořadí switcheru (indexu) vyhodnotí, jakou pozici v mřížce má mít. Vrátí row : int a column : int."""
        column = index % 4 + 1
        row = floor(index / 4) + self.details_rows
        return row, column

    def _clickedButton(self, index):
        """Metoda nastavující hodnoty a pozadí tlačítek při jejich zmáčknutí."""
        if self.selected_buttons[index] == 0:
            self.selected_buttons[index] = 1
            self.gym_details_widgets[index+1].configure(fg_color = "dodgerblue4")
        else:
            self.selected_buttons[index] = 0
            self.gym_details_widgets[index+1].configure(fg_color = "gray")

    def _createRun(self) -> None:
        """Metoda pro vytvoření grafiky pro filtraci distance běhu."""
        self.run_rows = 1
        self._distanceSportsFilterWidgets("Běh délka")
        # zvýšení řádku pro následné generování dalšího nastavení
        self.details_rows = self.details_rows + self.run_rows
        # pole všech grafických objektů funkce
        self.run_details_widgets = [self.run_l, self.from_l, self.from_e, self.to_l, self.to_e]
        
    def _createSwim(self) -> None:
        """Vytvoří widgety pro filrtraci  podrobností plaveckého tréninku."""
        self.swim_rows = 1
        self._distanceSportsFilterWidgets("Uplaváno")
        # zvýšení řádku pro následné generování dalšího nastavení
        self.details_rows = self.details_rows + self.swim_rows
        # pole všech grafických objektů funkce
        self.swim_details_widgets = [self.run_l, self.from_l, self.from_e, self.to_l, self.to_e]

    def _distanceSportsFilterWidgets (self, title : str) -> None:
        """Vytvoří widgety pro sporty, které v nastavení sportů mají možnost filtrovat vzdálenost."""
        self.var_from = StringVar()
        self.var_to = StringVar()
        self.run_l = Label(self, "{0}:".format(title), ("Arial", 10))
        self.run_l.grid(row=self.details_rows, column=0)
        self.run_l.configure(width=80)
        self.from_l = Label(self, "Od:", ("Airal", 10))
        self.from_l.grid(row = self.details_rows, column = 1)
        self.from_l.configure(width=30)
        self.from_e = Entry(self, self.var_from)
        self.from_e.grid(row=self.details_rows, column = 2)
        self.from_e.configure(height = 20, width=35)
        self.to_l = Label(self, "Do:", ("Airal", 10))
        self.to_l.grid(row = self.details_rows, column = 3)
        self.to_l.configure(width=30)
        self.to_e = Entry(self, self.var_to)
        self.to_e.grid(row=self.details_rows, column = 4)
        self.to_e.configure(height = 20, width=35)

    def _filteredGym(self) -> list:
        """Pokud bylo použito filtrování cviků v posilovně, funkce vrátí filtrované hodnoty."""
        return self.selected_buttons

    def _filteredRun(self) -> list:
        """Vrátí filtrované hodnoty běhu."""
        if self.run_details_widgets:
            distances = [self.var_from.get(), self.var_to.get()]
        return distances
    
    def _filteredSwim (self) -> list:
        """Vrátí filtrované hodnoty plavání."""
        if self.swim_details_widgets:
            distances = [self.var_from.get(), self.var_to.get()]
        return distances