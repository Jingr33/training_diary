#import knihoven
import customtkinter as ctk
from tkinter import *
#import souborů
from ctkWidgets import Frame, Label, Button, Entry
from configuration import gym_body_parts, sport_list


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
        self.gui_functions = [self._createGym, self._createRun]
        # cyklus přes všechny sporty, které se dají vyselectovat
        for i in range(len(selected_sports)):
            # pokud je sport vybraný...
            if int(selected_sports[i]) == 1: 
                # ...spustí se funkce generování jeho podrobného nastavení
                self.gui_functions[i]()

    def filtered(self):
        """Vrátí hodnoty zvolené ve filtru detailů sportů."""
        gym_values = self._filteredGym()
        run_values = self._filteredRun()
        filtered = [gym_values, run_values]
        return filtered

    def _createGym(self):
        """Metoda pro vytvoření grafiky pro filtraci jednotlivých části těla."""
        self.gym_rows = 2

        # inicializace grafiky
        self.label = Label(self, "Části těla: ", font=("Arial", 10))
        self.label.grid(row = self.details_rows, column=0)
        self.label.configure(width = 30)

        self.leg_b = Button(self, gym_body_parts[0], self._clickedLegButton)
        self.leg_b.grid(row = self.details_rows, column = 1, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.leg_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W, fg_color = "dodgerblue4")

        self.core_b = Button(self, gym_body_parts[1], self._clickedCoreButton)
        self.core_b.grid(row = self.details_rows, column = 2, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.core_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W, fg_color = "dodgerblue4")

        self.breast_b = Button(self, gym_body_parts[2], self._clickedBreastButton)
        self.breast_b.grid(row = self.details_rows, column = 3, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.breast_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W, fg_color = "dodgerblue4")

        self.shoulders_b = Button(self, gym_body_parts[3], self._clickedShoulderButton)
        self.shoulders_b.grid(row = self.details_rows, column = 4, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.shoulders_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W, fg_color = "dodgerblue4")

        self.back_b = Button(self, gym_body_parts[4], self._clickedBackButton)
        self.back_b.grid(row = self.details_rows+1, column = 1, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.back_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W, fg_color = "dodgerblue4")

        self.biceps_b = Button(self, gym_body_parts[5], self._clickedBicepsButton)
        self.biceps_b.grid(row = self.details_rows+1, column = 2, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.biceps_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W, fg_color = "dodgerblue4")

        self.triceps_b = Button(self, gym_body_parts[6], self._clickedTricepsButton)
        self.triceps_b.grid(row = self.details_rows+1, column = 3, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.triceps_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W, fg_color = "dodgerblue4")

        self.forearm_b = Button(self, gym_body_parts[7], self._clickedForearmButton)
        self.forearm_b.grid(row = self.details_rows+1, column = 4, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.forearm_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W, fg_color = "dodgerblue4")

        #pole nul pro přidávání  zvolených částí těla při filtrování
        self.selected_buttons = [1] * len(gym_body_parts)

        # zvýšení řádku pro následné generování dalšího nastavení
        self.details_rows = self.details_rows + self.gym_rows

        # pole všech grafických objektů funkce
        self.gym_details_widgets = [self.label, self.leg_b, self.core_b, self.breast_b, self.shoulders_b,
                               self.back_b, self.biceps_b, self.triceps_b, self.forearm_b]
        
    """Metody jednotlivých tlačítek odcvičených částí při zmáčknutí."""
    def _clickedLegButton(self):
        self._clickedButton(0)
    def _clickedCoreButton(self):
        self._clickedButton(1)
    def _clickedBreastButton(self):
        self._clickedButton(2)
    def _clickedShoulderButton(self):
        self._clickedButton(3)
    def _clickedBackButton(self):
        self._clickedButton(4)
    def _clickedBicepsButton(self):
        self._clickedButton(5)
    def _clickedTricepsButton(self):
        self._clickedButton(6)
    def _clickedForearmButton(self):
        self._clickedButton(7)

    def _clickedButton(self, index):
        """Metoda nastavující hodnoty a pozadí tlačítek při jejich zmáčknutí."""
        if self.selected_buttons[index] == 0:
            self.selected_buttons[index] = 1
            self.gym_details_widgets[index+1].configure(fg_color = "dodgerblue4")
        else:
            self.selected_buttons[index] = 0
            self.gym_details_widgets[index+1].configure(fg_color = "gray")


    def _filteredGym(self) -> list:
        """Pokud bylo použito filtrování cviků v posilovně, funkce vrátí filtrované hodnoty."""
        return self.selected_buttons

    def _createRun(self):
        """Metoda pro vytvoření grafiky pro filtraci distance běhu."""
        self.run_rows = 1

        self.var_from = StringVar()
        self.var_to = StringVar()

        self.run_l = Label(self, "Běh délka:", ("Arial", 10))
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

        # zvýšení řádku pro následné generování dalšího nastavení
        self.details_rows = self.details_rows + self.run_rows

        # pole všech grafických objektů funkce
        self.run_details_widgets = [self.run_l, self.from_l, self.from_e,
                                    self.to_l, self.to_e]
        
    def _filteredRun(self) -> list:
        """Vrátí filtrované hodnoty běhu."""
        if self.run_details_widgets:
            distances = [self.var_from.get(), self.var_to.get()]
        return distances