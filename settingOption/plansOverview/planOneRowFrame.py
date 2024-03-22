# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from general import General
from ctkWidgets import Label, Button, Frame
from configuration import colors


class PlanOneRowFrame (Frame):
    """Vytvoří jeden řádek (údaje o 1 tréninkovém plánu) v tabulce přehledu tréninkových plánů v nastavení aplikace."""
    def __init__(self, master, plan_loader : object, plan_index : int, row_index : int):
        super().__init__(master)
        self. master = master
        self.row_index = row_index
        text = ["{0}.".format(self.row_index)]
        plan_data = plan_loader.getOnePlanData(plan_index)
        self.all_plan_info = text + plan_data 
        self.plan_data = plan_loader.getOnePlanData(plan_index)
        self.info_labels = [None] * 4
        self._initInfoWidgets()
        self.button_state = 0
        self._initDeleteButton()

    def _initInfoWidgets (self) -> None:
        """Vytvoří labely inforumjící o tréninkovém plánu."""
        padx = 3
        pady = 3
        width = [70, 70, 70, 100]
        self.columnconfigure([0, 1, 2, 3, 4], weight = 1)
        for column in range(4):
            label = Label(self, self.all_plan_info[column])
            label.grid(row = 0, column = column, sticky = ctk.W, padx = padx, pady = pady)
            label.configure(width = width[column])
            self.info_labels[column] = label

    def _initDeleteButton (self) -> None:
        """Vytvoří button pro vymazání tréninkového plánu."""
        pady = 3
        padx = 3
        self.delete_button = Button(self, "Odstranit", self._deleteRow)
        self.delete_button.grid(row = 0, column = 4, padx = padx, pady = pady)
        self.delete_button.configure(width = 90, fg_color = colors["dodger-blue-3"], hover_color = colors["dodger-blue-2"])

    def _deleteRow (self) -> None:
        """Přepne tréninkový plán do disabled módu připraveného k odstranění."""
        if self.button_state == 0:
            self.button_state = 1
            General.setWidgetForeColor(self.delete_button, colors["dark-red"], colors["dark-red-hover"])
            for i in range(len(self.info_labels)):
                self.info_labels[i].configure(state = DISABLED)
            ...
            # dodělej funkčnost
        else:
            self.button_state = 0
            General.setWidgetForeColor(self.delete_button, colors["dodger-blue-3"], colors["dodger-blue-2"])
            for i in range(len(self.info_labels)):
                self.info_labels[i].configure(state = NORMAL)
            ...
            # dodělej funkčnost

        # možná bych ještě zkusil, pro oddělení řádků, ať se střídají světlé a tmavé pozadí framů s řádky
