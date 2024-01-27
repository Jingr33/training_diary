# import knihoven
from tkinter import *
import customtkinter as ctk
# importy souborů
from ctkWidgets import Frame
from createPlan.cyclePlan.cyclePlanFrame import CyclePlanFrame
from createPlan.singlePlan.singlePlanFrame import SinglePlanFrame

class SetPlanWindow (ctk.CTkToplevel):
    """Vytvoří okno pro nastavení tréninkového plánu v cyklickém režimu."""
    def __init__(self, master : ctk.CTkBaseClass, choice : int):
        self.choice = choice
        super().__init__(master)
        self.master = master
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self._kill)
        self.geometry("750x600")
        self.resizable(False, False)

        # slovník s možnostmi různých tréninkových plánů
        self.choice_dict = {
            0 : CyclePlanFrame(self),
            1 : SinglePlanFrame(self),
        }
        # vytvoření framu
        self._initPlanFrame()

    def backToChoiceWindow (self) -> None:
        """Vrátí uživatele na frame s výběrem typu tréninkového plánu."""
        # zobrazí původní okno
        self.master.deiconify()
        # zničí sebe
        self._kill()

    def _initPlanFrame (self) -> None:
        """Vytvoření framu s cyklickým plánem."""
        frame = self.choice_dict[self.choice]
        frame.pack(fill = ctk.BOTH, expand = True)
        frame.configure(corner_radius = 0, fg_color = "transparent")

    def _kill (self) -> None:
        """Vypne kono."""
        self.destroy()