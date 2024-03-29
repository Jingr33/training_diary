#importy knihoven
from tkinter import *
import customtkinter as ctk
from icecream import ic
#importy souborů
from ctkWidgets import Frame, Label
from createPlan.cyclePlan.oneActivity import OneActivity


class OneDayFrame (Frame):
    """Frame pro jeden den v náhledovém kalendáři nastavení cyklického tréninkového plánu.."""
    def __init__(self, master : ctk.CTkBaseClass, number_of_day : int):
        super().__init__(master)
        self.number_of_day = number_of_day
        self.number_of_frame = number_of_day - 1
        # list aktivit v dni
        self.activity_list = []

        # vytvoření obsahu
        self._createGUI()

    def dayReindexation (self, label_number : str) -> None:
        """Přepíše čísla dní v případě, že se nějaký z předchozích framů vymazal."""
        self.day_number.configure(width=100, text = label_number)

    def initFreeDayLabel(self) -> None:
        """Vytvoří label s nápisem "volný den" v případě zvolení chcecboxu volný den."""
        self.free_day_label = Label(self, "Volný den")
        self.free_day_label.pack(side=TOP, fill=ctk.BOTH, expand=True)

    def destroyFreeDayLabel(self) -> None:
        """Vymaže label s nápisem "volný den" v případě odklinutí chcecboxu volný den."""
        self.free_day_label.destroy()

    def addStrip (self, selected_sport : str, data_tuple : tuple) -> None:
        """Přidá strip s tréninkem do kalendáře."""
        one_activity = OneActivity(self, selected_sport, data_tuple)
        one_activity.pack(side=TOP, fill = ctk.X, padx = 2, pady=2)
        self.activity_list.append(one_activity)

    def _createGUI(self) -> None:
        """Grafický obsah."""
        # pomocný label, aby nastavil minimální výšku framu
        assist_label = Label(self, "")
        assist_label.pack(side=LEFT, pady = 3)
        assist_label.configure(height=100)
        # label s číslem dne
        self.day_number = Label(self, str(self.number_of_day))
        self.day_number.pack(side=TOP, padx=5, pady=5)
        self.day_number.configure(width=100)
