# importy knihoven
import customtkinter as ctk
from tkinter import *
from tkcalendar import Calendar
import datetime
# importy souborů
from ctkWidgets import Button
from ctkWidgets import Label
from ctkWidgets import Entry
from ctkWidgets import ChcekBox


class Frame (ctk.CTkFrame):
    """Frame pro nastavování údajů o jednotlivých trénincích."""
    def __init__(self, master: ctk.CTkBaseClass, choice) -> None:
        super().__init__(master)
        self.choice = choice
        today = datetime.date.today()

        # zadnání data tréninku
        date_l = Label(self, "Datum")
        date_l.pack(anchor=ctk.W)
        self.date_calendar = Calendar(self, selectmode = 'day', 
                               year = today.year, month = today.month, 
                               day = today.day)
        self.date_calendar.pack(side=TOP, padx=3, pady=3)

        # vytvoření GUI podle vybraného sportu
        self.createGui(self.choice)

        # tlačítko pro uložení tréninku
        save_b = Button(self, "Uložit", self.saveNewTraining)
        save_b.pack(side=BOTTOM, ipadx=7, ipady=7, padx=3, pady=3)


    def createGui (self, choice):
        """Metoda pro výběr GUI, které se vytvoří podle vybrané aktivity."""
        if choice == "posilovna":
            self.initGym()
        elif choice == "běh":
            self.initRun()
        else:
            ... #TODO

    def initGym (self):
        """Vytvoření nastavovacích okének pro přidání tréninku POSILOVNA."""
        # inicializace proměnných
        self.var_time = StringVar()
        self.var_legs = StringVar(value=0)
        self.var_core = StringVar(value=0)
        self.var_breast = StringVar(value=0)
        self.var_shoulders = StringVar(value=0)
        self.var_back = StringVar(value=0)
        self.var_biceps = StringVar(value=0)
        self.var_triceps = StringVar(value=0)
        self.var_forearm = StringVar(value=0)

        # zadání doby běhu
        Label(self, 'Čas').pack(anchor=ctk.W)
        Entry(self, self.var_time).pack(anchor=ctk.W)

        # vytvoření checkboxů s odcvičenými částmi
        exercise_l = Label(self, "Odcvičeno")
        exercise_l.pack(anchor=ctk.W)
        leg_chb = ChcekBox(self, 'Nohy', self.var_legs)
        leg_chb.pack(anchor=ctk.W)
        core_chb = ChcekBox(self, 'Střed těla', self.var_core)
        core_chb.pack(anchor=ctk.W)
        breast_chb = ChcekBox(self, 'Prsa', self.var_breast)
        breast_chb.pack(anchor=ctk.W)
        shoulders_chb = ChcekBox(self, 'Ramena', self.var_shoulders)
        shoulders_chb.pack(anchor=ctk.W)
        back_chb = ChcekBox(self, 'Záda', self.var_back)
        back_chb.pack(anchor=ctk.W)
        biceps_chb = ChcekBox(self, 'Biceps', self.var_biceps)
        biceps_chb.pack(anchor=ctk.W)
        triceps_chb = ChcekBox(self, 'Triceps', self.var_triceps)
        triceps_chb.pack(anchor=ctk.W)
        forearm_chb = ChcekBox(self, 'Předloktí', self.var_forearm)
        forearm_chb.pack(anchor=ctk.W)


    def initRun (self):
        """Vytvoření nastavovacích okének pro přidání tréninku BĚH."""
        #inicializace proměnných
        self.var_time = ctk.StringVar()
        self.var_length = ctk.StringVar()

        # zadání doby běhu
        Label(self, 'Čas (min)').pack(anchor=ctk.W)
        Entry(self, self.var_time).pack(anchor=ctk.W)

        # zadání kilometrů
        Label(self, 'Kilometry (km)').pack(anchor=ctk.W)
        Entry(self, self.var_length).pack(anchor=ctk.W)


    def saveNewTraining(self):
        """Funkce se spustí po stiknutí tlačítka uložit.
           Uloží data do souboru."""
        # list se zadanými údaji
        self.training_list = [self.choice, self.date_calendar.get_date()]

        # vyplnění training_listu podle zvoleného tréninku
        if self.training_list[0] == "posilovna":
            self.training_list.extend([self.var_legs.get(), self.var_core.get(),
                                       self.var_breast.get(), self.var_shoulders.get(),
                                       self.var_back.get(), self.var_biceps.get(),
                                       self.var_triceps.get(), self.var_forearm.get()])
        elif self.training_list[0] == "běh":
            self.training_list.extend([self.var_time.get(), self.var_length.get()])
        else:
            ... #TODO

        # příprava stringů na zapsání do souboru
        prepared_string = self.prepareString(self.training_list)

        # zapsání dat do souboru
        self.writeToFile(prepared_string)

        self.destroy()


    def prepareString(self, list):
        """Metoda pro přípravu stringu (řádku) pro zapsání do souboru."""
        string = self.training_list[1] + " / " +  self.training_list[0]

        for i in range(2, len(list)):
            string = string + " / " + list[i]

        # vrácení připraveného stringu
        return string


    def writeToFile (self, string):
        """Metoda pro zapsání dat do souboru."""
        with open("training_database.txt", 'a') as f:  
            f.write(string + "\n")

####################################
    def hello(self):
        print("hello")
