# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from sports.setSport import SetSport
from ctkWidgets import Frame
from general import General


class SetDetailsFrame (Frame):
    """Vytvoří frame v nastavení jednoduchého tréninkového plánu pro nastavení podrobností 
    jednotlivých tréninků."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.entry_width = 80

    def initWidgets (self, sport : str) -> None:
        """Vytvoří widgety pro zadání podrobností daného sportu."""
        General.deleteFrameWidgets(self)
        SetSport.singlePlanDetails(self, sport)