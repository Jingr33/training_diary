# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from settingOption.plansOverview.plansOverviewFrame import PlansOverviewFrame


class PlansOverviewWindow (ctk.CTkToplevel):
    """Toplevel window zobrazující přehled tréninkových plánů v nastavení aplikace."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.title("Přehled tréninkových plánů")
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self._kill)
        self.geometry("550x300")
        self.resizable(False, False)
        self._initContent()

    def _initContent (self) -> None:
        """Vytvoření obsahu okna přehledu tréninkových plánů."""
        plan_frame = PlansOverviewFrame(self)
        plan_frame.pack(side=TOP, fill = ctk.BOTH, expand = True)

    def _kill (self):
        """Zavření okna."""
        self.destroy()