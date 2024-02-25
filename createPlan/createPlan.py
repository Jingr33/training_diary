#importy knihoven
import customtkinter as ctk
from tkinter import *
# importy souborů
from createPlan.setPlanWindow import SetPlanWindow 
from ctkWidgets import Button
from configuration import colors


class CreatePlan (ctk.CTkToplevel):
    """Vytvoří Toplevel okno pro nastavení tréninkového plánu (při kllinutí na "Nastavit plán".)"""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.title('Výběr tréninkového plánu')
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self._kill)
        self.geometry("500x400")
        # vxtvoření grafického rozhraní
        self._createGui()

    def _createGui(self) -> None:
        ipadx = 40
        ipady = 20
        pady = 5
        """Vytvoří grafický obsah okna."""
        # tlačítko pro vytvoření tréninkového cyklu
        cycle = Button(self, "Vytvořit tréninkový cyklus", self._trainingCycle)
        cycle.pack(ipadx = ipadx, ipady = ipady, pady = pady)
        cycle.configure(fg_color = colors["light-gray"])
        # tlačítko pro vytvoření jednotlivých tréninků
        single = Button(self, "Plán jednotlivých tréninků", self._singleTraining)
        single.pack(ipadx = ipadx, ipady = ipady, pady=pady)
        single.configure(fg_color = colors["light-gray"])

    def _trainingCycle (self) -> None:
        """Spustí okno pro přidání plánu tréninkového cyklu a původní okno vypne."""
        # spuštění nastavovacího okna
        choice = 0 # -> znamená, že se zvolí varianta cyklyckých tréninků
        SetPlanWindow(self, choice)
        # skrytí aktuálního okna, ale zachování jeho existence
        self.withdraw()

    def _singleTraining (self) -> None:
        """Otevře okno pro přidání jednotlivých tréninků a původní okno smaže."""
        #spuštění nastavovacího okna
        choice = 1 # vybere se frame pro single training
        SetPlanWindow(self, choice)
        # vypnutí aktuálního okna
        self.withdraw()

    def _kill(self) -> None:
        """Zničí okno."""
        self.destroy()
