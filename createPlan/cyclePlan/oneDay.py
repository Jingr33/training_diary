#import knihoven
from tkinter import *
import customtkinter as ctk
from icecream import ic
#import souborů
from createPlan.cyclePlan.oneDayFrame import OneDayFrame
from createPlan.cyclePlan.sportDetailsFrame import SportDetailsFrame
from ctkWidgets import CheckBox, Button, Frame, ComboBox
from configuration import colors
import globalVariables as GV

class OneDay(Frame):
    """Třída pro soubor widgetů a kalendářového návrhu pro jeden den."""
    def __init__(self, master , day_number):
        super().__init__(master)
        self.master = master
        self.day_number = day_number
        self.frame_number = day_number - 1
        self.details_frame = 0
        # list vsech widgetů
        self.all_widgets = []
        # volný den
        self.free = False
        # grafika
        self._createGUI()

    def dayReindexation (self) -> None:
        """Přeindexování dne při vymazaní jiného dne."""
        self.frame.dayReindexation(str(self.day_number))

    def addTrainingToCalendar (self) -> None:
        """Uloží nastavená data a přidá trénink do náhledového kalendáře."""
        # získání dat zadaných v nastavení
        data_tuple = self.details_frame.getData()
        # ověření, že všechny vložená data jsou platná
        if self._detailsFrameVerifier(data_tuple):
            self.details_frame.destroy()
            # vybraný sport v comoboboxu
            selected_sport = self.var_text_cb.get()
            self.sports_cb.set(self.text_unknow)
            # vytvoření stripu v kalendáři (a uložení dat o tréninku)
            self.frame.addStrip(selected_sport, data_tuple)
        else:
            self.details_frame.errorAnimation()


    def _createGUI(self) -> None:
        """Vytvoření grafické widgety."""
        # frame dne
        self.frame = OneDayFrame(self, self.day_number)
        self.frame.pack(side=TOP, padx=2, pady=2, ipadx=3, ipady=3)
        self.frame.configure(fg_color=colors["light-gray"], corner_radius = 10)
        self.all_widgets.append(self.frame)

        # odstranění dne
        self.remove_button = Button(self, "Odstranit", self._removeFrame)
        self.remove_button.pack(side = TOP, padx=2, pady=2)
        self.remove_button.configure(height = 13, width=115, font=("Arial", 11))
        self.all_widgets.append(self.remove_button)

        # chceckbox - volný den
        self.var_free = StringVar(value = 0)
        free_day = CheckBox(self, "Volný den", self.var_free)
        free_day.pack(side=TOP, padx=2, pady=2, ipady=3)
        self.all_widgets.append(free_day)
        # event pro chceckbox
        free_day.bind("<Button-1>", self._setFreeDay)

        # nastavení podrobností tréninkové aktivity
        self._setSport()

    def _removeFrame (self) -> None:
        """Vymaže celý frame """
        self.master._removeFrame(self.frame_number)

    def _setFreeDay(self, arg) -> None:
        """Nastaví prvky okna pro volný den / zrušení volného dne."""
        if self.var_free.get() == "1":
            self._configFreeDay() # nastavení volného dne
        else:
            self._unconfigFreeDay() # odnastavení volného dne

    def _configFreeDay(self) -> None:
        """Nastavení konfigurace widgetů ve dni pro volný den."""
        self.free = True # nastavení, že je den volný
        self.frame.initFreeDayLabel() # vytvoření labelu s nápisem volno
        # self.remove_button.configure(state = "disabled") # tlačítko odstranit na disabled
        self.sports_cb.destroy() # zničení comboboxu se sporty
        if self.details_frame:
            self.details_frame.destroy()
        # skrytí aktivit ve dni
        if self.frame.activity_list:
            for strip in self.frame.activity_list:
                strip.pack_forget()

    def _unconfigFreeDay(self) -> None:
        """Nastavení konfigurace widgetů ve dni pro tréninkový den
        (resp. zrušení volného dne)"""
        self.free = False # Nastavení, že den není volný
        self.frame.destroyFreeDayLabel() # odstranění labelu s nápise volno
        # self.remove_button.configure(state = "enabled") # tlačítko odstranit na enabled
        self._setSport() # vytvoření comboboxu se sporty
        if self.frame.activity_list: # navrácení  stripů s aktivitami v pokud exitovaly
            for strip in self.frame.activity_list: 
                strip.pack(side=TOP, fill = ctk.X, padx = 2, pady=2)


    def _setSport (self) -> None:
        """Vytvoří combobox s výběrem sportů."""
        # combobox se sporty
        self.text_unknow = "nevybráno"
        self.var_text_cb = StringVar() # zapíše co uživatel vybral
        self.sports_cb = ComboBox(self, GV.sport_list, self._setSportDetails, self.var_text_cb)
        self.sports_cb.pack(side = TOP, padx=2, pady=2)
        self.sports_cb.configure(width = 115)
        self.sports_cb.set(self.text_unknow)
        self.all_widgets.append(self.sports_cb)

    def _sportElected (self, option) -> None:
        """Po vybrání sportu v comboBoxu se zavolájí potřebné funkce a vyvolají reakci.
        (strip v kalendáři)"""
        ... #TODO tohle ještě dodělat

    def _setSportDetails(self, option) -> None:
        """Vytvoří frame s nastavením detailů vybraného sportu."""
        # vymazání předchozího
        if self.details_frame:
            self.details_frame.destroy() #TODO - přepsat na fci
        # vytvoření framu pro obsah
        self.details_frame = SportDetailsFrame(self, str(option))
        self.details_frame.pack(side=TOP, padx=2, pady=2, ipadx=10, ipady=20)
        self.details_frame.configure(corner_radius = 6, width = 115)

    def _detailsFrameVerifier(self, data : tuple) -> bool:
        """Ověří, zda jsou zadaná data platná a vrátí bool."""
        verify = True
        for entry in data:
            if entry == None:
                verify = False
        return verify