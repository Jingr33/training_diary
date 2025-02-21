#importy knihoven
from tkinter import *
import customtkinter as ctk
# importy souborů
from configuration import unknown_text


class Sport():
    """Obecné funkce specifické pro jednotlivé sporty."""
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
            if entry == "" or entry == unknown_text:
                return unknown_text
            else:
                return None
            
    @staticmethod
    def emptyCheckboxChecker(values : list) -> list:
        """Ověří, zda byly ve skupině chcecboxů zakliknuty některé chceckbuttony
          nebo všechny zůstaly prázné."""
        for value in values:
            if value == "1":
                return values
        return [unknown_text]
    
    @staticmethod
    def plan_FreeDayDataToList(training : object) -> list:
        """Zapíše vlastnosti tréninku posilovna do listu."""
        data_list = [training.date, training.sport]
        return data_list
    
    @staticmethod
    def hasAttribute (object : object, attribute : str, negative) -> str:
        """Metoda ověří, zda má objekt atribut, pokud ano, vrátí ho, pokud ne, vrátí negative."""
        if hasattr(object, attribute):
            return getattr(object, attribute)
        else:
            return negative