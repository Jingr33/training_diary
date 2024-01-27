#import knihoven
from tkinter import *
import customtkinter as ctk
#import souborů
from createPlan.cyclePlan.dayDetailFrame import DayDetailFrame
from createPlan.cyclePlan.sportDetailsFrame import SportDetailsFrame
from ctkWidgets import CheckBox, Button, Frame, ComboBox
from configuration import colors, sport_list

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
        # grafika
        self._createGUI()

    def dayReindexation (self) -> None:
        """Přeindexování dne při vymazaní jiného dne."""
        self.frame.dayReindexation(str(self.day_number))


    def _createGUI(self) -> None:
        """Vytvoření grafické widgety."""
        # frame dne
        self.frame = DayDetailFrame(self, self.day_number)
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

        # nastavení podrobností
        self._setSport()

    def _removeFrame (self) -> None:
        """Vymaže celý frame """
        self.master._removeFrame(self.frame_number)

    def _setFreeDay(self, arg) -> None:
        """NAstaví prvky okna pro volný den."""
        if self.var_free.get() == "1":
            self.frame.initFreeDayLabel() # vytvoření labelu s nápisem volno
            self.remove_button.configure(state = "disabled") # tlačítko odstranit na disabled
            self.sports_cb.destroy() # zničení comboboxu se sporty
            if self.details_frame:
                self.details_frame.destroy()
        else:
            self.frame.destroyFreeDayLabel() # odstranění labelu s nápise volno
            self.remove_button.configure(state = "enabled") # tlačítko odstranit na enabled
            self._setSport() # vytvoření comboboxu se sporty

    def _setSport (self) -> None:
        """Vytvoří combobox s výběrem sportů."""
        # combobox se sporty
        self.text_unknow = "nevybráno"
        self.sports_cb = ComboBox(self, sport_list, self._setSportDetails, "nevybráno")
        self.sports_cb.pack(side = TOP, padx=2, pady=2)
        self.sports_cb.configure(width = 115)
        self.sports_cb.set(self.text_unknow)
        self.all_widgets.append(self.sports_cb)

    def _setSportDetails(self, option) -> None:
        """Vytvoří frame s nastavením detailů vybraného sportu."""
        # vymazání předchozího
        if self.details_frame:
            self.details_frame.destroy()
        # vytvoření framu pro obsah
        self.details_frame = SportDetailsFrame(self, str(option))
        self.details_frame.pack(side=TOP, padx=2, pady=2, ipadx=10, ipady=20)
        self.details_frame.configure(corner_radius = 6, width = 115)
