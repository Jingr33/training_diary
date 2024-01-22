# importy knihoven
from tkinter import *
import customtkinter as ctk
# importy souborů
from ctkWidgets import Frame, Label


class OneDayFrame (Frame):
    """Frame pro vyobrazení jednoho dne v grafickém kalendáři."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)

        # inicializace obsahu
        self._initGUI()

    def _initGUI(self) -> None:
        """Inicializace obsahu framů jednotlivých dní."""
        # tenhle label je tam jen proto abych nejak nastavil vysku tech ctverecku,
        # jinak v nem nic neni
        assist_label = Label(self, "")
        assist_label.pack(side=LEFT, ipady = 50)

        # label s datem
        self.label = Label(self, "1", ("Arial", 13))
        self.label.pack(fill = ctk.X, ipadx = 55)
        

