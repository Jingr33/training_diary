# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from sports.setSport import SetSport
from ctkWidgets import Frame
from general import General
from configuration import unknown_text


class SetDetailsFrame (Frame):
    """Vytvoří frame v nastavení jednoduchého tréninkového plánu pro nastavení podrobností 
    jednotlivých tréninků."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.entry_width = 80
        self.frame_data = []

    def initWidgets (self, sport : str) -> None:
        """Vytvoří widgety pro zadání podrobností daného sportu."""
        self.sport = sport
        General.deleteFrameWidgets(self)
        SetSport.singlePlanDetails(self, self.sport)

    def checkEntry (self) -> bool:
        """Ověří uživatelské vstupy podle zvoleného sportu."""
        return SetSport.singlePlanEntry(self, self.sport)
    
    def getData (self) -> list:
        """Získá data zadaná uživatelem do framu a přidá je k listu dat o podrobnostech tréninku z rodičovského objektu."""
        if self.frame_data[0] == "":
            self.frame_data[0] == unknown_text
        return self.frame_data