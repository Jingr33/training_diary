# import knihoven
from tkinter import *
import customtkinter as ctk
from icecream import ic
# import souborů
from settingOption.plansOverview.loadPlansData import LoadPlansData
from settingOption.plansOverview.planOneRowFrame import PlanOneRowFrame
from ctkWidgets import Label, Button

class PlansOverviewFrame (ctk.CTkScrollableFrame):
    """Frame s widgety přehledu tréninkových plánů (nastavení aplikace)."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.configure(corner_radius = 0, fg_color = "transparent")
        self.row_index = 0
        self.padx = (3, 8)
        self.pady = 3
        self.last_padx = (20, 150)
        self.columnconfigure([0,1,2,3], weight = 1)
        self.plan_loader = LoadPlansData(self) # načtení tréninkových plánů
        self._initLegend()
        self._initContent()

    def getPlanStates (self) -> list:
        """Vrátí 2 listy s hodnotami ke každému plánu o tom, zda má být vymazán nebo ponechán v databázi."""
        cycle = [self.all_rows[i].button_state for i in range(len(self.all_rows)) if self.all_rows[i].plan_type == "Cyklický"]
        single = [self.all_rows[i].button_state for i in range(len(self.all_rows)) if self.all_rows[i].plan_type == "Jednoduchý"]
        return cycle, single

    def _initLegend (self) -> None:
        """Vytvoření widget ve framu."""
        width = 70
        number_label = Label(self, "Pořadí", ("Arial", 13, "bold"))
        number_label.grid(row = 0, column = 0, padx = self.padx, pady = self.pady)
        number_label.configure(width = width)
        type_label = Label(self, "Typ", ("Arial", 13, "bold"))
        type_label.grid(row = 0, column = 1, padx = self.padx, pady = self.pady)
        type_label.configure(width = width)
        start_label = Label(self, "Začátek", ("Arial", 13, "bold"))
        start_label.grid(row = 0, column = 2, padx = self.padx, pady = self.pady)
        start_label.configure(width = width)
        others_label = Label(self, "Další", ("Arial", 13, "bold"))
        others_label.grid(row = 0, column = 3, padx = self.last_padx, pady = self.pady)
        others_label.configure(width = width)
        #index řady
        self.row_index = self.row_index + 1

    def _initContent(self) -> None:
        """Vytvoří jednotlivé framy (řádky) s térninkovými plány."""
        row_number = self.plan_loader.getNumberOfPlans()
        self.all_rows = [None] * row_number
        for i in range(row_number):
            one_row = PlanOneRowFrame(self, self.plan_loader, i, self.row_index)
            one_row.grid(row = self.row_index, column = 0, columnspan = 4, sticky = "NSEW")
            self.row_index = self.row_index + 1
            self.all_rows[i] = one_row