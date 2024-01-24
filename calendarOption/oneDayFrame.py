# importy knihoven
from tkinter import *
import customtkinter as ctk
# importy souborů
from ctkWidgets import Frame, Label
from configuration import sport_color
from calendarOption.oneStrip import OneStrip


class OneDayFrame (Frame):
    """Frame pro vyobrazení jednoho dne v grafickém kalendáři."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.strips = []

        # inicializace obsahu
        self._initGUI()

    def createStrip (self, training : object) -> None:
        """Vytvoření stripu pro trénink a uložení do pole stripů."""
        strip = OneStrip(self, training, ("Arial", 13))
        strip.pack(side=TOP, fill=ctk.X)
        strip.configure(width=15, fg_color = sport_color[training.sport], corner_radius = 8,
                        padx = 2, pady = 2)
        # přidání stripu do pole (využije se při promazávání stripů)
        self.strips.append(strip)

    def _initGUI(self) -> None:
        """Inicializace obsahu framů jednotlivých dní."""
        # tenhle label je tam jen proto abych nejak nastavil vysku tech ctverecku,
        # jinak v nem nic neni
        assist_label = Label(self, "")
        assist_label.pack(side=LEFT, ipady = 50)
        assist_label.configure(fg_color = "transparent")

        # label s datem
        self.label = Label(self, "1", ("Arial", 13))
        self.label.pack(fill = ctk.X, ipadx = 200)
        self.label.configure(fg_color = "transparent", corner_radius = 8)
