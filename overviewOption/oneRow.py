# inport knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from ctkWidgets import Label


class OneRow (ctk.CTkFrame):
    """Třída vytvoří jeden řádek tréninku v tabulce v přehledu tréninků."""
    def __init__(self, master: ctk.CTkBaseClass, one_training):
        super().__init__(master)
        self.training = one_training

        self._initGUI()

    def _initGUI(self):
        """Metoda pro vytvření obsahu jednoho řádku v tabulce s daty o tréninku."""
        # label s datem tréninku
        date_l = Label(self, self.training.date)
        date_l.pack(side = LEFT, fill = ctk.Y)
        date_l.configure(width = 100, height = 40)

        sport_l = Label(self, self.training.sport)
        sport_l.pack(side = LEFT, fill = ctk.Y)
        sport_l.configure(width = 110, height = 40, anchor = ctk.W)

        if self.training.sport == "posilovna":
            self.gymDetails()
        elif self.training.sport == "běh":
            self.runDetails()

    def gymDetails (self):
        """Metoda pro vytvoření specifických údajů o posilovně do tabulky."""
        time_l = Label(self, self.training.time)
        time_l.pack(side = LEFT, fill = ctk.Y)
        time_l.configure(width = 70, height = 40, anchor = ctk.W)

        practiced_l = Label(self, self.training.practicedParts)
        practiced_l.pack(side = LEFT, fill = ctk.Y)
        practiced_l.configure(width = 250, height = 40, anchor = ctk.W)

    def runDetails (self):
        """Metoda pro vytvoření specifických údajů o běhu do tabulky."""
        time_l = Label(self, self.training.time)
        time_l.pack(side = LEFT, fill = ctk.Y)
        time_l.configure(width = 70, height = 40, anchor = ctk.W)

        practiced_l = Label(self, self.training.distance)
        practiced_l.pack(side = LEFT, fill = ctk.Y)
        practiced_l.configure(width = 250, height = 40, anchor = ctk.W)
