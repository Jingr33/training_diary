# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from ctkWidgets import Frame, Label, Entry
from configuration import colors


class PersonalDataFrame (Frame):
    """Načte frame s nastavením osobních údajů."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.columnconfigure([0, 1, 2, 3], weight = 1)
        self._initGUI()

    def _initGUI(self) -> None:
        """Vytvoří grafucké rozhraní framu s nastavením osobních údajů."""
        # nadpis
        title_pad = 6
        title = Label(self, "Osobní údaje", ("Arial", 17))
        title.grid(row = 0, column = 0, sticky = ctk.W, columnspan = 4, padx = (15, title_pad), pady = title_pad)
        title.configure(text_color = colors["light"])
        # vstupy
        padx = 3
        pady = 2
        mass_label = Label(self, "Hmotnost:")
        mass_label.grid(row = 1, column = 0, sticky = ctk.E, padx = padx)
        self.var_mass = StringVar()
        mass_entry = Entry(self, self.var_mass)
        mass_entry.grid(row = 1, column = 1, sticky = ctk.W, padx = padx, pady = pady)
        mass_entry.configure(width = 140)
        height_label = Label(self, "Výška:")
        height_label.grid(row = 1, column = 2, sticky = ctk.E, padx = padx)
        self.var_height = StringVar()
        height_entry = Entry(self, self.var_mass)
        height_entry.grid(row = 1, column = 3, sticky = ctk.W,padx = padx, pady = pady)
        height_entry.configure(width = 140)
        age_label = Label(self, "Věk:")
        age_label.grid(row = 2, column = 0, sticky = ctk.E, padx = padx)
        self.var_age = StringVar()
        age_entry = Entry(self, self.var_mass)
        age_entry.grid(row = 2, column = 1, sticky = ctk.W,padx = padx, pady = pady)
        age_entry.configure(width = 140)
        gender_label = Label(self, "Pohlaví:")
        gender_label.grid(row = 2, column = 2, sticky = ctk.E, padx = padx)
        self.var_gender = StringVar()
        gender_entry = Entry(self, self.var_mass)
        gender_entry.grid(row = 2, column = 3, sticky = ctk.W,padx = padx, pady = pady)
        gender_entry.configure(width = 140)