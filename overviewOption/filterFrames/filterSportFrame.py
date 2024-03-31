#import knihoven
import customtkinter as ctk
from tkinter import *
from icecream import ic
#import souborů
from ctkWidgets import Frame, CheckBox
from configuration import all_sports
import globalVariables as GV


class FilterSport (Frame):
    """Frame pro filtrování sportu."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self._initCheckboxes()

    def _initCheckboxes (self) -> None:
        """Vytvoří checkboxy pro zakliknutí sportů, které se mají vyfiltrovat."""
        self.chb_vars = [None] * len(all_sports)
        self.checkboxes = [None] * len(all_sports)
        for i in range(len(all_sports)):
            var = StringVar(value = 1)
            chb = CheckBox(self, all_sports[i], var)
            chb.pack(side = TOP, pady = 1)
            if all_sports[i] in GV.sport_list:
                chb.select()
            self.chb_vars[i] = var
            self.checkboxes[i] = chb

    def filtered (self):
        """Vrátí hodnoty zakliknuté ve filtru sportu."""
        values = [var.get() for var in self.chb_vars]
        return values
