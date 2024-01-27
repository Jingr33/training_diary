# importy knihoven
from tkinter import *
import customtkinter as ctk
#importy souborů
from ctkWidgets import Frame, Button, Label, Entry
from createPlan.cyclePlan.planCalendar import PlanCalendar

class CyclePlanFrame (Frame):
    """Frame s nastavení cycklického tréninkového plánu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master

        # nastavení mřížky
        self.columnconfigure([0, 1, 2, 3], weight=1)
        self.rowconfigure([0, 2, 3], weight = 1)
        self.rowconfigure(1, weight=200)
        self.rowconfigure(4, weight=2)

        self._initBackButton() # tlačítko zpět
        self._initGui() # základní nastavení
        self._initDetailsFrame() # vnořený frame
        self._initSaveButton() # ukládací tlačítko

    def _initBackButton (self) -> None:
        """Talčítko zpět."""
        back_button = Button(self, "Zpět", self.master.backToChoiceWindow)
        back_button.grid(row=0, column=0, sticky="NW")
        back_button.configure(width=40)


    def _initGui (self) -> None:
        """Vytvoření grafického prostředí."""
        # proměnné pro uživatelské vstupy
        self.var_start = StringVar()
        self.var_end = StringVar()
        self.var_cycles = StringVar()

        #paddingy
        padx = 7

        # widgety
        start_l = Label(self, "Začátek (dd/mm/yyyy): ")
        start_l.grid(row=2, column=0, pady=padx, sticky="E")

        self.start_e = Entry(self, self.var_start)
        self.start_e.grid(row=2, column=1, pady=padx)

        end_l = Label(self, "Konec (dd/mm/yyyy): ")
        end_l.grid(row=2, column=2, pady=padx, sticky="E")

        self.end_e = Entry(self, self.var_end)
        self.end_e.grid(row=2, column=3, pady=padx)

        cycles_l = Label(self, "Počet cyklů: ")
        cycles_l.grid(row = 3, column = 0, pady=padx, sticky="E")

        self.cycles_e = Entry(self, self.var_cycles)
        self.cycles_e.grid(row=3, column=1, pady=padx)

    def _initDetailsFrame (self) -> None:
        """Vygenerování framu s naastavením detailních údajů."""
        #paddingy
        padx_frame = 3
        pady_frame = 3

        details_frame = PlanCalendar(self)
        details_frame.grid(row=1, column=0, columnspan = 5, sticky="NSWE", 
                           padx = padx_frame, pady = pady_frame)
        details_frame.configure(corner_radius=6)

    def _initSaveButton (self) -> None:
        """Vytvoří tlačítko "uložit"."""
        save_button = Button(self, "Uložit", self._savePlan)
        save_button.grid(row=5, column=3, pady = 4)
        save_button.configure(height=30)

    def _savePlan(self):
        """Uloží tréninkový nový plán."""
        ...
        