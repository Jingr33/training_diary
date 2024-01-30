#importy knihoven
from tkinter import *
import customtkinter as ctk
# importy souborů


class Sport():
    """Obecné funkce pro jakékoliv typy tréninků."""
    def __init__(self):
        ...

    def createAttributes(self) -> list:
        """List názvů atributů tréninku vypisujících se do tooltipů."""
        self.message_values = []

    def createValues(self) -> list:
        self.message_attributes = []

    def tooltipMessage(self) -> str:
        """Metoda pro vytvoření zprávy zobrazující se v tooltipu v kalendáři."""
        message = self.message_values[1].upper() + ": \n"
        for i in range(2, len(self.message_attributes)):
            message = message + self.message_attributes[i] + ": " + self.message_values[i] + "\n"
        return message
    
    @staticmethod
    def floatEntryChecker(entry : str) -> str:
        """Ověří zda se dá vstup převést na int nebo je neplatný nebo nezadaný
        a vrátí výsledek."""
        try:
            float(entry)
            return entry
        except:
            if entry == "":
                return "nezadáno"
            else:
                return None