# importy knihoven
import customtkinter as ctk
from tkinter import *
from tkcalendar import Calendar
import datetime
# importy souborů
from ctkWidgets import Button
from ctkWidgets import Label
from ctkWidgets import Entry
from ctkWidgets import CheckBox
from configuration import sport_list, trainings_path, gym_body_parts


class Frame (ctk.CTkScrollableFrame):
    """Frame pro nastavování údajů o jednotlivých trénincích."""
    def __init__(self, master: ctk.CTkBaseClass) -> None:
        super().__init__(master)
        self.today = datetime.date.today()

    def initWidgets (self, choice) -> None:
        """Inicializuje widgety framu v závislosti na výběru sportu."""
        self.choice = choice
        # inicializace proměnných které potřebuju mít uložené v každém případě
        self.var_time = ctk.StringVar()
        self.var_length = ctk.StringVar()

        # zadnání data tréninku
        date_l = Label(self, "Datum")
        date_l.pack(anchor=ctk.W)
        date_l.configure(corner_radius = 8)
        self.date_calendar = Calendar(self, selectmode = 'day', 
                               year = self.today.year, month = self.today.month, 
                               day = self.today.day)
        self.date_calendar.pack(side=TOP, padx=3, pady=3)

        # vytvoření GUI podle vybraného sportu
        self._sportWidgets(self.choice)

        # tlačítko pro uložení tréninku
        self.save_b = Button(self, "Uložit", self._saveNewTraining)
        self.save_b.pack(side=BOTTOM, ipadx=7, ipady=7, padx=3, pady=3)


    def _sportWidgets (self, choice):
        """Metoda pro výběr GUI, které se vytvoří podle vybrané aktivity."""
        if choice == sport_list[0]:
            self._initGym()
        elif choice == sport_list[1]:
            self._initRun()
        else:
            ... #TODO

    def _initGym (self):
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
        leg_chb = CheckBox(self, gym_body_parts[0], self.var_legs)
        leg_chb.pack(anchor=ctk.W)
        core_chb = CheckBox(self, gym_body_parts[1], self.var_core)
        core_chb.pack(anchor=ctk.W)
        breast_chb = CheckBox(self, gym_body_parts[2], self.var_breast)
        breast_chb.pack(anchor=ctk.W)
        shoulders_chb = CheckBox(self, gym_body_parts[3], self.var_shoulders)
        shoulders_chb.pack(anchor=ctk.W)
        back_chb = CheckBox(self, gym_body_parts[4], self.var_back)
        back_chb.pack(anchor=ctk.W)
        biceps_chb = CheckBox(self, gym_body_parts[5], self.var_biceps)
        biceps_chb.pack(anchor=ctk.W)
        triceps_chb = CheckBox(self, gym_body_parts[6], self.var_triceps)
        triceps_chb.pack(anchor=ctk.W)
        forearm_chb = CheckBox(self, gym_body_parts[7], self.var_forearm)
        forearm_chb.pack(anchor=ctk.W)

    def _initRun (self):
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

    def _saveNewTraining(self):
        """Funkce se spustí po stiknutí tlačítka uložit.
           Uloží data do souboru."""
        # ověření vstupů
        verify = self.floatEntryVerify(self.var_time.get(), self.var_length.get())
        if verify:
            # úprava zápisu data
            formated_date = self._editDateFormat(self.date_calendar.get_date())
            # list se zadanými údaji
            self.training_list = [self.choice, formated_date]

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

    def _editDateFormat(self, original_date :str) -> str:
        """Metoda pro přepsaní data z formátu tkinterového 
        kalendáře do formátu českého zápisu data."""
        # převedení údajů (měsíc, datum, rok) do listu
        mmddyyyy = original_date.split("/")

        # přidání 0 před číslo, pokud je menší než 10
        for i in range(len(mmddyyyy)):
            if int(mmddyyyy[i]) < 10:
                mmddyyyy[i] = "0" + mmddyyyy[i]

        # vytvoření stringu s českým datem
        formated_date = mmddyyyy[1] + ". " + mmddyyyy[0] + ". " + mmddyyyy[2]
        return formated_date

    def prepareString(self, list):
        """Metoda pro přípravu stringu (řádku) pro zapsání do souboru."""
        string = self.training_list[1] + " / " +  self.training_list[0]

        for i in range(2, len(list)):
            string = string + " / " + list[i]

        # vrácení připraveného stringu
        return string


    def writeToFile (self, string):
        """Metoda pro zapsání dat do souboru."""
        with open(trainings_path, 'a') as f:  
            f.write(string + " / \n")


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
        alert_b = Button(self, "OK", self._confirmationAlertDestroy)
        alert_b.configure(fg_color = "green", hover_color = "#109116")
        alert_b.pack()

    def _confirmationAlertDestroy(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()
        self.pack_forget()