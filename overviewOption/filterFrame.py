# import knihoven
from tkinter import *
import customtkinter as ctk
from icecream import ic
# import souborů
from ctkWidgets import Button
from ctkWidgets import Button
from overviewOption.filter import Filter
from overviewOption.filterFrames.filterDateFrame import FilterDate
from overviewOption.filterFrames.filterSportFrame import FilterSport
from overviewOption.filterFrames.filterTimeFrame import FilterTime
from overviewOption.filterFrames.filterDetailsFrame import FilterDetails
from general import General
from configuration import sport_list, gym_body_parts


class FilterFrame (ctk.CTkScrollableFrame):
    """Vytvoří Frame pro zaklikávání možností filtrování v přehledu tréninků."""
    def __init__(self, master :ctk.CTkBaseClass, trainings):
        super().__init__(master)
        self.master = master
        self.trainings = trainings
        # nastavení scrollbaru, aby nebyl moc velký
        self.configure(height = 120)
        self._scrollbar.configure(height = 0)

        # vytvoření grafického rozhraní
        self._createGUI()

        # eventy pro přidávání a oddělávání podrobného nastavení
        self._bindEvents()
        ####################################
        # detail_filter_funcs = [self.gymFilterSelected, self.runFilterSelected, self.swimFilterSelected]
        # self._bindEvents(detail_filter_funcs)
        ###########################################
        # self.filter_sport.gym_chb.bind('<Button-1>', self.gymFilterSelected)
        # self.filter_sport.run_chb.bind('<Button-1>', self.runFilterSelected)

    def _createGUI(self) -> None:
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

    def _filter(self) -> None:
        """Spuštění filtrování při kliknutí na tlačítko filtrovat."""
        #stažení hodnot o filtrování datumu
        date_filter = self.filter_date.filtered()
        # stažení hodnot filtrování sportu
        sport_filter = self.filter_sport.filtered()
        # stažení hodnot o filtrování času
        time_filter = self.filter_time.filtered()
        # stažení hodnot o filtrování detailů sportů
        detail_filter = self.filter_details.filtered()

        # zavolání vyfiltrování
        self.filter = Filter(self.trainings, date_filter, sport_filter, time_filter, detail_filter)
        self.filtered_data = self.filter.getFilteredData()

        # přegenerování tabulky s vyfiltrovanýchmi tréninky
        self.master.Filtering()

    def getData (self) -> list:
        """Metoda vrátí vyfiltrovaná data."""
        return self.filtered_data

    def _bindEvents (self) -> None:
        """Přidá eventy k podrobnostím filtrů, aby se skryly v případě, že sport není vybrán."""
        for i in range(len(self.filter_sport.chb_vars)):
            self.filter_sport.checkboxes[i].bind('<Button-1>', lambda value: self._filterSelected(i))
###########################################################
    # def _bindEvents (self, detail_filter_function : list) -> None:
    #     """Přidá eventy k podrobnostím filtrů, aby se skryly v případě, že sport není vybrán."""
    #     for i in range(len(self.filter_sport.chb_vars)):
    #         self.filter_sport.checkboxes[i].bind('<Button-1>', lambda value: detail_filter_function[i](i))
    
    def _filterSelected (self, index : int) -> None:
        """Přidá nebo odebere podrobné nastavení filtrace tréninků typu, který byl právě změněn do opačného stavu (zapnut, vypnut)"""
        if int(self.filter_sport.chb_vars[index].get()) == 0:
            General.deleteListWidgets(self.filter_details.gym_details_widgets)
        else: # zavolání funkce pro přerenderivání grafického rozhraní
            self.sportWasSelected()
#################################################################
    # def gymFilterSelected (self, index : int) -> None:
    #     """Metoda pro přidání podrobného nastavení pro tréninky v posilovně."""
    #     ic(int(self.filter_sport.chb_vars[index].get()) == 0)
    #     if int(self.filter_sport.chb_vars[index].get()) == 0:
    #         General.deleteListWidgets(self.filter_details.gym_details_widgets)
    #     elif int(self.filter_sport.var_gym.get()) == 1:
    #         # zavolání funkce pro přerenderivání grafického rozhraní
    #         self.sportWasSelected()

    # def runFilterSelected (self, index : int) -> None:
    #     """Metoda pro přidání podrobného nastavení pro běžecké tréninky."""
    #     print("zde")
    #     ic(int(self.filter_sport.chb_vars[index].get()) == 0)
    #     if int(self.filter_sport.chb_vars[index].get()) == 0:
    #         General.deleteListWidgets(self.filter_details.run_details_widgets)
    #     elif int(self.filter_sport.var_run.get()) == 1:
    #         # zavolání funkce pro přerenderování grafického rozhraní
    #         self.sportWasSelected()

    # def swimFilterSelected (self, index : int) -> None:
    #     """Metoda pro přidání podrobného nastavení pro plavecké tréninky."""
    #     ...

    def sportWasSelected(self) -> None:
        """Metoda pro vyvolání pře-renderování detailního nastavení při vybrání 
        kteréhokoliv sportu."""
        General.deleteFrameWidgets(self.filter_details)
        # proměnná s listem se sporty, které byly vyselectovány
        selected = self.filter_sport.filtered()
        ic(selected)
        # znovu-vyrenderování vybraných nastavovacích oken
        self.filter_details.createAllGUI(selected)

#################################################
        #TODO - poklikej filtry a uvidíš v těch výpisech, že ti nejede plavání tak jak má, to je první co máš opravit
#################################################



