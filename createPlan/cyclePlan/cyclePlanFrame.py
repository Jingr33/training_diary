# importy knihoven
from tkinter import *
import customtkinter as ctk
#importy souborů
from ctkWidgets import Frame, Button, Label, Entry
from createPlan.cyclePlan.planCalendar import PlanCalendar
from sports.setSport import SetSport
from general import General
from configuration import plans_path

class CyclePlanFrame (Frame):
    """Frame s nastavení cycklického tréninkového plánu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.error_l = None # proměnná pro erorovou hlášku

        # nastavení mřížky
        self.columnconfigure([0, 1, 2, 3], weight=1)
        self.rowconfigure([0, 2, 3, 4], weight = 1)
        self.rowconfigure(1, weight=200)
        self.rowconfigure(5, weight=2)

        self._initBackButton() # tlačítko zpět
        self._initGui() # základní nastavení
        self._initDetailsFrame() # vnořený frame
        self._initSaveButton() # ukládací tlačítko

        # bool proměnné -> True = ověřený vstup
        self.start_verified = False
        self.end_verified = False
        self.cycle_verified = False

        # eventy pro ověřévání vstupů
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

        self.details_frame = PlanCalendar(self)
        self.details_frame.grid(row=1, column=0, columnspan = 5, sticky="NSWE", 
                           padx = padx_frame, pady = pady_frame)
        self.details_frame.configure(corner_radius=6)

    def _initSaveButton (self) -> None:
        """Vytvoří tlačítko "uložit"."""
        save_button = Button(self, "Uložit", self._savePlan)
        save_button.grid(row=5, column=3, pady = 4)
        save_button.configure(height=30)

    def _savePlan(self):
        """Uloží tréninkový nový plán."""
        # ověření platnosti vstupů
        self._verifyStart(self.var_start)
        self._verifyEnd(self.var_end)
        self._verifyCycle(self.var_cycles)
        # vyhodnocení platnosti vstupů
        if self.start_verified and self.end_verified and self.cycle_verified:
            # smazání chybové hlášky
            self._savePlanErrorDestroy()
            # list z datových údajů
            main_info_list = [self.start, self.end, self.cycles]
            # stažení dat z náhledového kalendáře
            training_list = self._loadCalendarData()
            print(training_list)
            # uložení dat
            self._writeDataToFile(main_info_list, training_list)
        else:
            self._savePlanError()

    def _loadCalendarData (self) -> list:
        """Stáhne data každého tréninku z kalendáře a vytvoří jejich list."""
        training_list = []
        # list uložených dní tréninkového plánu
        days = self.details_frame.days
        # cyklus přes dny
        for day in days:
            # list aktivit v jednom dni
            day_index = self.details_frame.day_number
            activities = day.frame.activity_list
            # cyklus přes aktivity
            for activity in activities:
                training = activity.one_training
                # nastavení dne
                training.date = day_index
                training_list.append(training)
        return training_list
    
    def _writeDataToFile (self, info : list, trainings : list) -> None:
        """Uloží tréninkové data do souboru."""
        #vytvoření prvního řádku se základními údaji do souboru
        first_line = General.prepareString(info)
        with open(plans_path, 'a') as f:
            f.write(first_line + "\n")
            # vytvoření ostaních řádků
            for training in trainings:
                # vytvoření listu údajů z vlastností objektu
                data_list = SetSport.plan_trainingToList(training)
                #zíkání stringu
                line = General.prepareString(data_list)
                # zapsání do souboru
                f.write(line + "\n")

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
        if entry == "":
            return True
        return General.checkDateEntry(entry)

    def _verifyCycle (self, value) -> None:
        """Získá a ověří vstupní hodnoty počtu cyklů tréninkového plánu."""
        # ověření počtu cyklů
        cycle_chceck = True
        if value != "":
            cycle_chceck = General.checkIntEntry(self.var_cycles.get())
        self._cycleCheckReaction(cycle_chceck)

    def _StartCheckReaction(self, date_check : bool) -> None:
        """Provede reakci na ověření vstupu počátečního data tréninkového plánu.
        Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        if date_check:
            self.start = self.var_start.get()
            self.start_error_l.configure(text = "")
            self.start_verified = True
        else:
            self.start_error_l.configure(text = "Špatné zadání.")

    def _EndCheckReaction(self, date_check : bool) -> None:
        """Provede reakci na ověření vstupu koncového data tréninkového plánu.
        Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        if date_check:
            self.end = self.var_end.get()
            self.end_error_l.configure(text = "")
            self.end_verified = True
        else:
            self.end_error_l.configure(text = "Špatné zadání.")


    def _cycleCheckReaction(self, cycle_chceck : bool) -> None:
        """Provede reakci na ověření vstupu počtu cyklů tréninkového plánu.
        Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        if cycle_chceck:
            self.cycles = self.var_cycles.get()
            self.cycle_error_l.configure(text = "*V případě nezadání konce", text_color = "gray")
            self.cycle_verified = True
        else:
            self.cycle_error_l.configure(text = "Špatné zadání.", text_color = "red")

    def _savePlanError (self) -> None:
        """Inicializuje erorovou hlášku, pokud byl formulář špatně vyplněn."""
        self.error_l = Label(self, "Nesprávně vyplněný formulář.", ("Arial", 12, "bold"))
        self.error_l.grid(row = 4, column = 3)
        self.error_l.configure(text_color = "red")

    def _savePlanErrorDestroy(self) -> None:
        """Vymaže erorovou hlášku pokud existovala."""
        if self.error_l:
            self.error_l.destroy()
