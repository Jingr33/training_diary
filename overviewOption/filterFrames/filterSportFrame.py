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
        self.var_gym = StringVar(value=1)
        self.var_run = StringVar(value=1)

        #vytvoření checkboxů pro zakliknnutí sportu
        self.gym_chb = CheckBox(self, sport_list[0], self.var_gym)
        self.gym_chb.pack(side=TOP, pady=1)
        self.gym_chb.select()
        self.run_chb = CheckBox(self, sport_list[1], self.var_run)
        self.run_chb.pack(side=TOP, pady=1)
        self.run_chb.select()

    def filtered(self):
        """Vrátí hodnoty zakliknuté ve filtru sportu."""
        values = [self.var_gym.get(), self.var_run.get()]
        return values
