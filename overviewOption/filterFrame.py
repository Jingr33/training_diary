# import knihoven
from tkinter import *
import customtkinter as ctk
from ctkWidgets import Frame, CheckBox, Label, Entry, Button
from overviewOption.filter import Filter
from overviewOption.filterFrames.filterDateFrame import FilterDate
from overviewOption.filterFrames.filterSportFrame import FilterSport
from overviewOption.filterFrames.filterTimeFrame import FilterTime
from overviewOption.filterFrames.filterDetailsFrame import FilterDetails
from configuration import sport_list, gym_body_parts


class FilterFrame (ctk.CTkFrame):
    """Vytvoří Frame pro zaklikávání možností filtrování v přehledu tréninků."""
    def __init__(self, master :ctk.CTkBaseClass, trainings):
        super().__init__(master)
        self.trainings = trainings

        # vytvoření grafického rozhraní
        self._createGUI()

        # eventy pro přidávání a oddělávání podrobného nastavení
        self.filter_sport.gym_chb.bind('<Button-1>', self.gymFilterSelected)
        self.filter_sport.run_chb.bind('<Button-1>', self.runFilterSelected)

    def _createGUI(self):
        """Vytvoření grafického rozraní."""
        self.filter_date = FilterDate(self)
        self.filter_date.pack(side=LEFT, fill=ctk.Y, ipadx=3)
        self.filter_date.configure(width = 100, height=100, corner_radius = 0, fg_color='transparent')

        self.filter_sport = FilterSport(self)
        self.filter_sport.pack(side=LEFT, fill=ctk.Y, ipadx=3)
        self.filter_sport.configure(width = 110, height=100, corner_radius = 0, fg_color='transparent')

        self.filter_time = FilterTime(self)
        self.filter_time.pack(side=LEFT, fill=ctk.Y, ipadx=3)
        self.filter_time.configure(width = 80, height=100, corner_radius = 0, fg_color='transparent')

        self.filter_details = FilterDetails(self)
        self.filter_details.pack(side=LEFT, fill = ctk.Y, ipadx=3, padx=10)
        self.filter_details.configure(width = 250, height=100, corner_radius = 0, fg_color='transparent')

        self.filter_button = Button(self, "Filtrovat", self._filter)
        self.filter_button.pack(side=RIGHT, ipadx=7, ipady=7, anchor=ctk.N, padx=10, pady=10)
        self.filter_button.configure(width=70)


    def _filter(self):
        """Spuštění filtrování při kliknutí na tlačítko filtrovat."""
        #TODO - stažení hodnot o filtrování data
        date_filter = self.filter_date.filtered()

        # stažení hodnot filtrování sportu
        sport_filter = self.filter_sport.filtered()

        # stažení hodnot o filtrování času
        time_filter = self.filter_time.filtered()

        # zavolání vyfiltrování
        self.filter = Filter(self.trainings, date_filter, sport_filter, time_filter)
        self.filtered_data = self.filter.getFilteredData()

    def getData (self):
        """Metoda vrátí vyfiltrovaná data."""
        return self.filtered_data
    
    def gymFilterSelected (self, master):
        """Metoda pro přidání podrobného nastavení pro tréninky v posilovně."""
        if int(self.filter_sport.var_gym.get()) == 0:
            # destroyne widgety posilovny
            for widget in self.filter_details.gym_details_widgets:
                widget.destroy()
        elif int(self.filter_sport.var_gym.get()) == 1:
            # zavolání funkce pro přerenderivání grafického rozhraní
            self.sportWasSelected()

    def runFilterSelected (self, master):
        """Metoda pro přidání podrobného nastavení pro běžecké tréninky."""
        if int(self.filter_sport.var_run.get()) == 0:
            # destroyne widgety běhu
            for widget in self.filter_details.run_details_widgets:
                widget.destroy()
        elif int(self.filter_sport.var_run.get()) == 1:
            # zavolání funkce pro přerenderivání grafického rozhraní
            self.sportWasSelected()

    def sportWasSelected(self):
        """Metoda pro vyvolání pře-renderování detailního nastavení pře vybrání 
        kteréhokoliv sportu."""
        # smazaní předchozího obsahu
        for widget in self.filter_details.winfo_children():
            widget.destroy()

        # proměnná s listem se sporty, které byly vyselectovány
        selected = self.filter_sport.filtered()
        # znovu-vyrenderování vybraných nastavovacích oken
        self.filter_details.createAllGUI(selected)



