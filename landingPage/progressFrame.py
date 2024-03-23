# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from image import Image as img
from ctkWidgets import Frame, Label
from configuration import colors


class ProgressFrame (Frame):
    def __init__ (self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self._initTitle()
        self._progressBars()

    def _initTitle (self) -> None:
        """Vytvoří obsahové (textové) widgety ve framu."""
        title = Label(self, "Vítej zpět!", ("Arial", 21, "bold"))
        title.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = "w")
        title.configure(text_color = colors["light"], fg_color = "transparent")

    def _progressBars (self) -> None:
        """vytvoří progresbary."""
        ...