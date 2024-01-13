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
        self.date_l = Label(self, "Datum")
        self.date_l.pack(anchor=ctk.W)
        self.date_e = Calendar(self, selectmode = 'day', 
                               year = today.year, month = today.month, 
                               day = today.day)
        self.date_e.pack(side=TOP, padx=3, pady=3)

        # vytvoření GUI podle vybraného sportu
        self.createGui(choice)

        # tlačítko pro uložení tréninku
        self.save_b = Button(self, "Uložit", self.saveNewTraining)
        self.save_b.pack(side=BOTTOM, ipadx=7, ipady=7, padx=3, pady=3)


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
        var_time = StringVar()
        var_legs = StringVar(value='on')
        var_core = StringVar(value='on')
        var_breast = StringVar(value='on')
        var_shoulders = StringVar(value='on')
        var_back = StringVar(value='on')
        var_biceps = StringVar(value='on')
        var_triceps = StringVar(value='on')
        var_forearm = StringVar(value='on')

        # zadání doby běhu
        Label(self, 'Čas').pack(anchor=ctk.W)
        Entry(self, var_time).pack(anchor=ctk.W)

        # vytvoření checkboxů s odcvičenými částmi
        exercise_l = Label(self, "Odcvičeno")
        exercise_l.pack(anchor=ctk.W)
        leg_chb = ChcekBox(self, 'Nohy', var_legs)
        leg_chb.pack(anchor=ctk.W)
        core_chb = ChcekBox(self, 'Střed těla', var_core)
        core_chb.pack(anchor=ctk.W)
        breast_chb = ChcekBox(self, 'Prsa', var_breast)
        breast_chb.pack(anchor=ctk.W)
        shoulders_chb = ChcekBox(self, 'Ramena', var_shoulders)
        shoulders_chb.pack(anchor=ctk.W)
        back_chb = ChcekBox(self, 'Záda', var_back)
        back_chb.pack(anchor=ctk.W)
        biceps_chb = ChcekBox(self, 'Biceps', var_biceps)
        biceps_chb.pack(anchor=ctk.W)
        triceps_chb = ChcekBox(self, 'Triceps', var_triceps)
        triceps_chb.pack(anchor=ctk.W)
        forearm_chb = ChcekBox(self, 'Předloktí', var_forearm)
        forearm_chb.pack(anchor=ctk.W)


    def initRun (self):
        """Vytvoření nastavovacích okének pro přidání tréninku BĚH."""
        #inicializace proměnných
        self.var_time = ctk.StringVar()
        self.var_length = ctk.StringVar()

        # zadání doby běhu
        Label(self, 'Čas').pack(anchor=ctk.W)
        Entry(self, self.var_time).pack(anchor=ctk.W)

        # zadání kilometrů
        Label(self, 'Kilometry').pack(anchor=ctk.W)
        Entry(self, self.var_length).pack(anchor=ctk.W)

    def saveNewTraining(self):
        ...

####################################
    def hello(self):
        print("hello")
