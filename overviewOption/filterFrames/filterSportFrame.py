#import knihoven
import customtkinter as ctk
from tkinter import *
#import souborů
from ctkWidgets import Frame, CheckBox
from configuration import sport_list


class FilterSport (Frame):
    """Frame pro filtrování sportu."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self._initCheckboxes()

    def _initCheckboxes (self) -> None:
        """Vytvoří checkboxy pro zakliknutí sportů, které se mají vyfiltrovat."""
        self.chb_vars = [None] * len(sport_list)
        self.checkboxes = [None] * len(sport_list)
        for i in range(len(sport_list)):
            var = StringVar(value = 1)
            chb = CheckBox(self, sport_list[i], var)
            chb.pack(side = TOP, pady = 1)
            chb.select()
            self.chb_vars[i] = var
            self.checkboxes[i] = chb

    def filtered (self):
        """Vrátí hodnoty zakliknuté ve filtru sportu."""
        values = [var.get() for var in self.chb_vars]
        ###################################################
        # values = [self.var_gym.get(), self.var_run.get()]
        return values
