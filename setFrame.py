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
from configuration import *


class Frame (ctk.CTkFrame):
    """Frame pro nastavování údajů o jednotlivých trénincích."""

    def __init__(self, master: ctk.CTkBaseClass, choice) -> None:
        super().__init__(master)
        self.choice = choice
        today = datetime.date.today()
        # inicializace proměnných které potřebuju mít uložené v každém případě
        self.var_time = ctk.StringVar()
        self.var_length = ctk.StringVar()

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
        self.save_b = Button(self, "Uložit", self.saveNewTraining)
        self.save_b.pack(side=BOTTOM, ipadx=7, ipady=7, padx=3, pady=3)


    def createGui (self, choice):
        """Metoda pro výběr GUI, které se vytvoří podle vybrané aktivity."""
        if choice == sport_list[0]:
            self.initGym()
        elif choice == sport_list[1]:
            self.initRun()
        else:
            ... #TODO

    def initGym (self):
        """Vytvoření nastavovacích okének pro přidání tréninku POSILOVNA."""
        # inicializace proměnných
        self.var_legs = StringVar(value=0)
        self.var_core = StringVar(value=0)
        self.var_breast = StringVar(value=0)
        self.var_shoulders = StringVar(value=0)
        self.var_back = StringVar(value=0)
        self.var_biceps = StringVar(value=0)
        self.var_triceps = StringVar(value=0)
        self.var_forearm = StringVar(value=0)

        # zadání času strtáveného v posilovně
        Label(self, 'Čas').pack(anchor=ctk.W)
        time_e = Entry(self, self.var_time)
        time_e.pack(anchor=ctk.W)
        self.time_error_l = Label(self, "", ("Arial", 10))
        self.time_error_l.pack(anchor=ctk.W, side=TOP)

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

        # zadání doby běhu
        Label(self, 'Čas (min)').pack(anchor=ctk.W)
        Entry(self, self.var_time).pack(anchor=ctk.W)
        self.time_error_l = Label(self, "", ("Arial", 10))
        self.time_error_l.pack(anchor=ctk.W, side=TOP)


        # zadání kilometrů
        Label(self, 'Kilometry (km)').pack(anchor=ctk.W)
        Entry(self, self.var_length).pack(anchor=ctk.W)
        self.distance_error_l = Label(self, "", ("Arial", 10))
        self.distance_error_l.pack(anchor=ctk.W, side=TOP)



    def saveNewTraining(self):
        """Funkce se spustí po stiknutí tlačítka uložit.
           Uloží data do souboru."""
        # ověření vstupů
        verify = self.floatEntryVerify(self.var_time.get(), self.var_length.get())

        if verify:
            # list se zadanými údaji
            self.training_list = [self.choice, self.date_calendar.get_date()]

            # vyplnění training_listu podle zvoleného tréninku
            if self.training_list[0] == sport_list[0]:
                self.training_list.extend([self.var_time.get(), self.var_legs.get(), self.var_core.get(),
                                        self.var_breast.get(), self.var_shoulders.get(),
                                        self.var_back.get(), self.var_biceps.get(),
                                        self.var_triceps.get(), self.var_forearm.get()])
            elif self.training_list[0] == sport_list[1]:
                self.training_list.extend([self.var_time.get(), self.var_length.get()])
            else:
                ... #TODO

            # příprava stringů na zapsání do souboru
            prepared_string = self.prepareString(self.training_list)

            # zapsání dat do souboru
            self.writeToFile(prepared_string)

            # vymazání framu
            for widget in self.winfo_children(): # odstranění widgetů
                widget.destroy()
            self.conmfirmationAlert(self.choice) # zobrazení potvrzovacího alertu



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


    def floatEntryVerify (self, try_time, try_distance):
        """Metoda pr ověření platnosti vstupů příp zadávání tréninku."""
        verify_time = False
        try:
            if try_time:
                float(try_time)
                self.time_error_l.configure(text = "")
            verify_time = True
        except:
            self.time_error_l.configure(text_color = 'red', text = "Špatně zadaná hodnota.")

        verify_distance = False
        try:
            if try_distance:
                float(try_distance)
                self.distance_error_l.configure(text = "")
            verify_distance = True
        except:
            self.distance_error_l.configure(text_color = 'red', text="Špatně zadaná hodnota.")

        return verify_time and verify_distance
    
    def conmfirmationAlert(self, choice):
        """Metoda pro zobrazení záverečné potvrzující zprávy o přidání tréninku."""

        # potvrzující zpráva
        message = "Trénink " + choice + " \nbyl přidán."
        alert_l = Label(self, message, ("Arial", 18))
        alert_l.configure(justify="center")
        alert_l.pack(padx=10, pady=10)

        # tlačítko pro zrušení alertu
        alert_b = Button(self, "OK", self.confirmationAlertDestroy)
        alert_b.configure(fg_color = "green", hover_color = "dark-green")
        alert_b.pack()

    def confirmationAlertDestroy(self):
        self.destroy()