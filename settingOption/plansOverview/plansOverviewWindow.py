# import knihoven
from tkinter import *
import customtkinter as ctk
from icecream import ic
# import souborů
from settingOption.plansOverview.plansOverviewFrame import PlansOverviewFrame
from configuration import cycle_plans_path, single_plans_path
from general import General


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
        self.plan_frame = PlansOverviewFrame(self)
        self.plan_frame.pack(side=TOP, fill = ctk.BOTH, expand = True)

    def _kill (self):
        """Zavření okna."""
        self._saveChanges()
        self.destroy()

    def _saveChanges (self) -> None:
        """Uloží změny do databáze tréninkových plánů."""
        # indexy plánu pro ponechání a vymazání
        cycle_states, single_states = self.plan_frame.getPlanStates()
        plan_states = {
            cycle_plans_path : cycle_states,
            single_plans_path : single_states,
        }
        for plan_path in (cycle_plans_path, single_plans_path):
            file_lines = General.loadLinesFromFile(plan_path)
            updated_lines = self._cutOutDeletedPlans(file_lines, plan_states[plan_path])
            with open (plan_path, "w+") as f:
                for line in updated_lines:
                    f.write(line + "\n")

    def _cutOutDeletedPlans (self, lines : list, plan_states : list) -> list:
        """Odstraní uživatelem smazané tréninkové plány a vrátí list řádků pro zpětné zapsání do souboru."""
        lines = self._trimLines(lines)
        last_line = 0
        for i in range(len(plan_states)): # cyklus přes všechny uložené tréninky
            if plan_states[i]:
                while lines[last_line] != ";":
                    last_line = last_line + 1
                last_line = last_line + 1
            else:
                while lines[last_line] != ";":
                    del lines[last_line]
                del lines[last_line]
        return lines

    def _trimLines (self, lines : list) -> list:
        """Odstraní přebytečné znaky z řádků."""
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "")
        return lines
