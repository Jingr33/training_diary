# importy knihoven
from tkinter import *
import customtkinter as ctk
#importy souborů
from ctkWidgets import Frame, Button, Label, Entry
from createPlan.cyclePlan.planCalendar import PlanCalendar
from general import General

class CyclePlanFrame (Frame):
    """Frame s nastavení cycklického tréninkového plánu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master

        # nastavení mřížky
        self.columnconfigure([0, 1, 2, 3], weight=1)
        self.rowconfigure([0, 2, 3, 4], weight = 1)
        self.rowconfigure(1, weight=200)
        self.rowconfigure(5, weight=2)

        self._initBackButton() # tlačítko zpět
        self._initGui() # základní nastavení
        self._initDetailsFrame() # vnořený frame
        self._initSaveButton() # ukládací tlačítko

        self.start_e.bind('<FocusOut>', self._verifyStart)
        self.end_e.bind('<FocusOut>', self._verifyEnd)
        self.cycles_e.bind('<FocusOut>', self._verifyCycle)

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
        pady = 7

        # widgety
        start_l = Label(self, "Začátek (dd/mm/yyyy): ")
        start_l.grid(row=2, column=0, pady=pady, sticky="E")

        self.start_e = Entry(self, self.var_start)
        self.start_e.grid(row=2, column=1, pady=pady)

        self.start_error_l = Label(self, "", ("Arial", 11))
        self.start_error_l.grid(row=3, column = 1, pady=pady)
        self.start_error_l.configure(text_color = "red", height = 10)

        end_l = Label(self, "Konec (dd/mm/yyyy): ")
        end_l.grid(row=2, column=2, pady=pady, sticky="E")

        self.end_e = Entry(self, self.var_end)
        self.end_e.grid(row=2, column=3, pady=pady)

        self.end_error_l = Label(self, "", ("Arial", 11))
        self.end_error_l.grid(row=3, column = 3, pady=pady)
        self.end_error_l.configure(text_color = "red", height = 10)

        cycles_l = Label(self, "Počet cyklů: ")
        cycles_l.grid(row = 4, column = 0, pady=pady, sticky="E")

        self.cycles_e = Entry(self, self.var_cycles)
        self.cycles_e.grid(row=4, column=1, pady=pady)

        self.cycle_error_l = Label(self, "*V případě nezadání konce", ("Arial", 11))
        self.cycle_error_l.grid(row=5, column = 1, pady=pady)
        self.cycle_error_l.configure(text_color = "gray")


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

    def _verifyStart (self, value) -> None:
        """Získá a ověří vstupní hodnoty začátku tréninkového plánu."""
        # ověření počátečního data
        date_check = self._dateChecker(self.var_start.get())
        self._StartCheckReaction(date_check)


    def _verifyEnd (self, value) -> None:
        """Získá a ověří vstupní hodnoty konce tréninkového plánu."""
        # ověření koncového data
        date_check = self._dateChecker(self.var_end.get())
        self._EndCheckReaction(date_check)

    def _dateChecker(self, entry : str) -> bool:
        """Ověří zda jde o platný vstup data formátu (dd/mm/yyyy)."""
        return General.checkDateEntry(entry)

    def _verifyCycle (self, value) -> None:
        """Získá a ověří vstupní hodnoty počtu cyklů tréninkového plánu."""
        # ověření počtu cyklů
        cycle_chceck = General.checkIntEntry(self.var_cycles.get())
        self._cycleCheckReaction(cycle_chceck)

    def _StartCheckReaction(self, date_check : bool) -> None:
        """Provede reakci na ověření vstupu počátečního data tréninkového plánu.
        Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        if date_check:
            self.start = self.var_start.get()
            self.start_error_l.configure(text = "")
        else:
            self.start_error_l.configure(text = "Špatné zadání.")

    def _EndCheckReaction(self, date_check : bool) -> None:
        """Provede reakci na ověření vstupu koncového data tréninkového plánu.
        Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        print(date_check)
        if date_check:
            self.end = self.var_end.get()
            self.end_error_l.configure(text = "")
        else:
            self.end_error_l.configure(text = "Špatné zadání.")


    def _cycleCheckReaction(self, cycle_chceck : bool) -> None:
        """Provede reakci na ověření vstupu počtu cyklů tréninkového plánu.
        Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        if cycle_chceck:
            self.cycles = self.var_cycles.get()
            self.cycle_error_l.configure(text = "*V případě nezadání konce", text_color = "gray")
        else:
            self.cycle_error_l.configure(text = "Špatné zadání.", text_color = "red")
