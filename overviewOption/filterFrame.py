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

        self.filter_button = Button(self, "Filtrovat", self.filter)
        self.filter_button.pack(side=RIGHT, ipadx=7, ipady=7, anchor=ctk.N, padx=10, pady=10)
        self.filter_button.configure(width=70)

    def filter(self) -> None:
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
        self.master.filtering()

    def getData (self) -> list:
        """Metoda vrátí vyfiltrovaná data."""
        return self.filtered_data

    def _bindEvents (self) -> None:
        """Přidá eventy k podrobnostím filtrů, aby se skryly v případě, že sport není vybrán."""
        for i in range(len(self.filter_sport.checkboxes)):
            self.filter_sport.checkboxes[i].bind('<Button-1>', lambda value: self.sportWasSelected())
    
    def sportWasSelected(self) -> None:
        """Metoda pro vyvolání pře-renderování detailního nastavení při vybrání 
        kteréhokoliv sportu."""
        General.deleteFrameWidgets(self.filter_details)
        # proměnná s listem se sporty, které byly vyselectovány
        selected = self.filter_sport.filtered()
        # znovu-vyrenderování vybraných nastavovacích oken
        self.filter_details.createAllGUI(selected)