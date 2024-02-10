# importy knihoven
import customtkinter as ctk
from tkinter import *
from tkcalendar import Calendar
import datetime
# importy souborů
from sports.setSport import SetSport
from ctkWidgets import Button, Label, Entry
from configuration import trainings_path, unknown_text
from general import General


class Frame (ctk.CTkScrollableFrame):
    """Frame pro nastavování údajů o jednotlivých trénincích."""
    def __init__(self, master: ctk.CTkBaseClass) -> None:
        super().__init__(master)
        self.today = datetime.date.today()

    def initWidgets (self, choice) -> None:
        """Inicializuje widgety framu v závislosti na výběru sportu."""
        self.choice = choice
        # vymazání předchozího
        General.deleteWidgets(self)
        # inicializace proměnných které potřebuju mít uložené v každém případě
        self.var_time = ctk.StringVar()
        self.var_distance = ctk.StringVar()
        # zadnání data tréninku
        date_l = Label(self, "Datum")
        date_l.pack(anchor=ctk.W)
        date_l.configure(corner_radius = 8)
        self.date_calendar = Calendar(self, selectmode = 'day', 
                               year = self.today.year, month = self.today.month, 
                               day = self.today.day)
        self.date_calendar.pack(side=TOP, padx=3, pady=3)
        # zadávání času
        self._initTimeEntry()
        # vytvoření GUI podle vybraného sportu
        SetSport.setFrameWidgets(self, choice)
        # tlačítko pro uložení tréninku
        self.save_b = Button(self, "Uložit", self._saveNewTraining)
        self.save_b.pack(side=BOTTOM, ipadx=7, ipady=7, padx=3, pady=3)

    def _initTimeEntry (self) -> None:
        """Vytvoří widgety pro zadání času."""
        Label(self, 'Čas').pack(anchor=ctk.W)
        time_e = Entry(self, self.var_time)
        time_e.pack(anchor=ctk.W)
        self.time_error_l = Label(self, "", ("Arial", 10))
        self.time_error_l.pack(anchor=ctk.W, side=TOP)

    def _saveNewTraining(self):
        """Funkce se spustí po stiknutí tlačítka uložit. Verifikuje vstupy.
           Uloží data do souboru."""
        # ověření vstupů
        verified = self._floatEntryVerify(self.var_time.get())
        if verified:
            self._getTrainingToFile()
            General.deleteWidgets(self)
            self._conmfirmationAlert(self.choice) # zobrazení potvrzovacího alertu
        else:
            ... #TODO špatné vstupy

    def _getTrainingToFile (self) -> None:
        """Uloží data do souboru ve správném formátu."""
        formated_date = self._editDateFormat(self.date_calendar.get_date()) # úprava zápisu data
        training_list = [formated_date, self.choice] # list se zadanými údaji
        SetSport.fillListForFile(self, training_list)
        training_list = self._isSetted(training_list)# při nezadání vstupu přidá neuvedeno
        prepared_string = General.prepareString(training_list)
        self._writeToFile(prepared_string)

    def _editDateFormat(self, original_date :str) -> str:
        """Metoda pro přepsaní data z formátu tkinterového 
        kalendáře do formátu českého zápisu data."""
        mmddyy = original_date.split("/")# převedení údajů (měsíc, datum, rok) do listu
        for i in range(len(mmddyy)):  # přidání 0 před číslo, pokud je menší než 10
            if int(mmddyy[i]) < 10:
                mmddyy[i] = "0" + mmddyy[i]
        # vytvoření stringu s českým datem
        formated_date = mmddyy[1] + ". " + mmddyy[0] + ". " + mmddyy[2]
        return formated_date

    def _writeToFile (self, string):
        """Metoda pro zapsání dat do souboru."""
        with open(trainings_path, 'a') as f:  
            f.write(string + " / \n")

    def _floatEntryVerify (self, time_entry : str) -> None:
        """Metoda pr ověření platnosti vstupů příp zadávání tréninku."""
        self.verify_time = self._timeVerify(time_entry)
        # verify_distance = self._distanceVerify(distance_entry)
        self.verify_details = SetSport.verifyDetails(self)
        return self.verify_time and self.verify_details
    
    def _timeVerify (self, time_entry : str) -> bool:
        """Ověří platnost vstupu času."""
        verify_time = False
        try:
            if time_entry:
                float(time_entry)
                self.time_error_l.configure(text = "")
            verify_time = True
        except:
            self.time_error_l.configure(text_color = 'red', text = "Špatně zadaná hodnota.")
        return verify_time

    def _isSetted (self, list : list) -> list:
        """Pro nezadané položky listu ("") zadá do proměnné, že údaj nebyl uveden. """
        for i in range(len(list)):
            list[i] = self._setUnknow(list[i])
        return list

    def _setUnknow (self, entry : str) -> None:
        """Nastavý zadaný parametr na neuvedený, pokud je užvatelský vstup prázdný."""
        if entry:
            return entry
        else:
            return unknown_text
    
    def _conmfirmationAlert(self, choice) -> None:
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