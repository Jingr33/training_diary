# importy knihoven
from tkinter import *
import customtkinter as ctk
from datetime import date
from icecream import ic
#importy souborů
from ctkWidgets import Frame, Button, Label, Entry
from createPlan.cyclePlan.planCalendar import PlanCalendar
from sports.setSport import SetSport
from oneTraining import OneTraining
from general import General
from configuration import cycle_plans_path

class CyclePlanFrame (Frame):
    """Frame s nastavení cycklického tréninkového plánu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.error_l = None # proměnná pro erorovou hlášku
        self.end = "" # pokud by byla hodnota nevyplněná
        self.cycles = ""

        # nastavení mřížky
        self.columnconfigure([0, 1, 2, 3], weight=1)
        self.rowconfigure([0, 2, 3, 4], weight = 1)
        self.rowconfigure(1, weight=200)
        self.rowconfigure(5, weight=2)

        General.initBackButton(self) # tlačítko zpět
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
        #koncové datum
        end_l = Label(self, "Konec (dd/mm/yyyy): ")
        end_l.grid(row=2, column=2, pady=pady, sticky="E")
        self.end_e = Entry(self, self.var_end)
        self.end_e.grid(row=2, column=3, pady=pady)
        self.end_error_l = Label(self, "", ("Arial", 11))
        self.end_error_l.grid(row=3, column = 3, pady=pady)
        self.end_error_l.configure(text_color = "red", height = 10)
        # počet cyklů
        cycles_l = Label(self, "Počet cyklů: ")
        cycles_l.grid(row = 4, column = 0, pady=pady, sticky="E")
        self.cycles_e = Entry(self, self.var_cycles)
        self.cycles_e.grid(row=4, column=1, pady=pady)
        self.cycle_error_l = Label(self, "*V případě nezadání konce", ("Arial", 11))
        self.cycle_error_l.grid(row=5, column = 1, pady=pady)
        self.cycle_error_l.configure(text_color = "gray")

    def _initDetailsFrame (self) -> None:
        """Vygenerování framu s nastavením detailních údajů."""
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
        # platnost vstupů
        self._entryVerify()
        # vyhodnocení platnosti vstupů
        entry_check = self.start_verified and self.end_verified and self.cycle_verified
        self.num_of_days = self._getNumOfDays() # získá počet dní cyklu
        days_check = self.num_of_days > 1
        if entry_check and days_check:
            # smazání chybové hlášky
            self._savePlanErrorDestroy()
            # list z datových údajů
            main_info_list = [self.start, self.end, self.cycles, self.num_of_days]
            # stažení dat z náhledového kalendáře
            training_list = self._loadCalendarData()
            # uložení dat
            self._writeDataToFile(main_info_list, training_list)
            # vyplnutí okna s nastavováním plánu
            self._killToplevel(self.master)
        else:
            self._savePlanError()

    def _loadCalendarData (self) -> list:
        """Stáhne data každého tréninku z náhledového kalendáře a vytvoří jejich list."""
        training_list = []
        # list uložených dní tréninkového plánu
        days = self.details_frame.days
        # cyklus přes dny
        for day in days:
            # list aktivit v jednom dni
            day_index = day.day_number
            activities = day.frame.activity_list
            # cyklus přes aktivity
            for activity in activities:
                training = activity.one_training
                # nastavení dne
                training.date = day_index
                training_list.append(training)
            # zjistí, zda se jedná o volný den
            if day.free:
                training_list = self._isFreeDay(day, training_list, day_index)
        return training_list
    
    def _isFreeDay(self, day : object, training_list : list, day_index : int) -> list:
        """Zjistí, zda se jedná o volný den.
        Ano -> přidá do dne s volnem aktivitu volno a vrátí ho.
        Ne -> nevrátí nic."""
        # pokud je den volný den -> provede se
        free_training = OneTraining(self)
        free_training.makeFreeDay()
        free_training.date = day_index
        training_list.append(free_training)
        return training_list
    
    def _writeDataToFile (self, info : list, trainings : list) -> None:
        """Uloží tréninkové data do souboru."""
        #vytvoření prvního řádku se základními údaji do souboru
        first_line = General.prepareString(info)
        with open(cycle_plans_path, 'a') as f:
            f.write(first_line + "\n")
            # vytvoření ostaních řádků
            for training in trainings:
                # vytvoření listu údajů z vlastností objektu
                data_list = SetSport.plan_trainingToList(training)
                #zíkání stringu
                line = General.prepareString(data_list)
                # zapsání do souboru
                f.write(line + "\n")
            f.write(";\n")

    def _getNumOfDays (self) -> None:
        """Získá počet dní, ze kterých je složen tréninkový plán."""
        return len(self.details_frame.days)
    
    def _killToplevel (self, master : object) -> None:
        """Vypne okna pro nastavování tréninkového plánu."""
        master.master.destroy()
        master.destroy()

    def _entryVerify(self) -> bool:
        """Finální ověření platnosti vstupů a jejich smysluplnosti."""
        self._verifyStart(self.var_start.get()) # ověření počátku
        self._verifyEnd(self.var_end.get()) # ověření oknce
        self._verifyCycle(self.var_cycles.get()) # ověření počtu cyklů
        self._CompareEntries() # smyslupnost dat

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
        cycle_chceck = False
        cycle_chceck = General.checkIntEntry(self.var_cycles.get())
        self._cycleCheckReaction(cycle_chceck)

    def _StartCheckReaction(self, date_check : bool) -> None:
        """Provede reakci na ověření vstupu počátečního data tréninkového plánu. Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        if date_check:
            self.start = self.var_start.get()
            self.start_error_l.configure(text = "")
            self.start_verified = True
        else:
            self.start_error_l.configure(text = "Špatné zadání.")
            self.cycle_verified = False

    def _EndCheckReaction(self, date_check : bool) -> None:
        """Provede reakci na ověření vstupu koncového data tréninkového plánu. Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        if date_check:
            self.end = self.var_end.get()
            self.end_error_l.configure(text = "")
            self.end_verified = True
        else:
            self.end_error_l.configure(text = "Špatné zadání.")
            self.end_verified = False

    def _cycleCheckReaction(self, cycle_chceck : bool) -> None:
        """Provede reakci na ověření vstupu počtu cyklů tréninkového plánu. Buď uloží zadanou hodnotu nebo napíše chybovou hlášku."""
        if cycle_chceck:
            self.cycles = self.var_cycles.get()
            self.cycle_error_l.configure(text = "*V případě nezadání konce", text_color = "gray")
            self.cycle_verified = True
        else:
            self.cycle_error_l.configure(text = "Špatné zadání.", text_color = "red")
            self.cycle_verified = False

    def _CompareEntries (self) -> None:
        """Vyhodnotí, zda zadaná data vůči sobě dávají smysl a zda nezadané údaje jsou nutné pro vytvoření tréninkového plánu."""
        # porovnání začátečního a koncového data
        self._startVsEndDate()
        # nezadání koncového data nebo počtu cyklů
        self._endOrCyclesForgive()

    def _startVsEndDate (self) -> None:
        """Vyhodnotí zda je počáteční datum dříve než koncové."""
        # proběhne pokud je vstup správný
        if self.start_verified and self.end_verified:
            #převedení na datum
            start_values = self.var_start.get().split("/")
            end_values = self.var_end.get().split("/")
            start = date(int(start_values[2]), int(start_values[1]), int(start_values[0]))
            end = date(int(end_values[2]), int(end_values[1]), int(end_values[0]))
            # pokud není začátek před koncem, ověření dat se nastaví na false
            if start > end:
                self.start_verified = False
                self.end_verified = False

    def _endOrCyclesForgive(self) -> None:
        """Zajišťuje možnost nevyplnění nepovinných polí."""
        if self.end_verified and self.var_cycles.get() == "":
            self.cycle_verified = True
        elif self.cycle_verified and self.var_end.get() == "":
            self.end_verified = True

    def _savePlanError (self) -> None:
        """Inicializuje erorovou hlášku, pokud byl formulář špatně vyplněn."""
        self.error_l = Label(self, "Nesprávně vyplněný formulář.", ("Arial", 12, "bold"))
        self.error_l.grid(row = 4, column = 3)
        self.error_l.configure(text_color = "red")

    def _savePlanErrorDestroy(self) -> None:
        """Vymaže erorovou hlášku pokud existovala."""
        if self.error_l:
            self.error_l.destroy()
