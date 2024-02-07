# import knihoven
import customtkinter as ctk
from tkinter import *
# import souborů
from calendarOption.oneDayFrame import OneDayFrame
from calendarOption.tableContentFiller import TabelContentFiller

class calendarTable (ctk.CTkScrollableFrame):
    """Vytvoří grafický kalendář jako čtvercovou soustavu framů."""
    def __init__(self, master :ctk.CTkBaseClass, date : tuple):
        super().__init__(master)
        self.master = master
        self.date = date
        self.prev_button = self.master.slider_frame.prev_b
        self.next_button = self.master.slider_frame.next_b

        # event pro resizování okna
        # self.bind('<Configure>', self._windowResize)

        # inicializace framové mřížky
        self._initGrid()

        # list s kalendářními daty jednotlivých polí
        self.fillDatesToTable()

        # eventy pro kliknutí na tlačítka nastavování měsíce (prev, next)
        self.prev_button.bind('<Button-1>', self.regenerateDates)
        self.next_button.bind('<Button-1>', self.regenerateDates)


    def _initGrid(self) -> None:
        """Metoda pro vytvoření framové mřížky (6 řádků, 7 sloupců)."""
        # 6 řádků, protože do více týdnů 1 měsíc nikdy nezasahuje
        # velikost přížky
        self.columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)
        self.columnconfigure([0, 1, 2, 3, 4, 5], weight = 1)
        #pole pro ukládání framů
        self.day_frames = [None] * 42
        i = 0
        for row in range(6): #přes řádky
            for column in range(7): #přes sloupce
                frame = OneDayFrame(self)
                frame.grid(row=row, column=column, ipadx = 2, ipady = 2, padx = 2, pady = 2)
                frame.configure(corner_radius = 5)
                self.day_frames[i] = frame
                i = i + 1

    def fillDatesToTable (self) -> None:
        """Metoda pro naplnění framů (jednotlivých dní) a jejich labelů daty dní, které obsahují."""
        self.table_filler = TabelContentFiller(self.date) # instance objektu plnícího tabulku daty
        dates_list = self.table_filler.dates_list # vytvoření listu s daty daného měsíce
        self.table_filler.datesToLabelsConfig(self.day_frames, dates_list) # zapsaní měsíců do framů
        self.table_filler.displayTrainingWidget(self.day_frames) #zapsání stripů s tréninky do kalendáře


    def regenerateDates (self, master) -> None:
        """Metoda pro přegenerování dat při přepnutí kalendáře na jiný měsíc.
        Eventová metoda od prev a next buttonů."""
        # uložení nového měsíce
        self.date = self.master.slider_frame.setted_date
        #přepsání dat v kalendáři
        self.fillDatesToTable()

############################################# tohle vůbec nepoužívám
    def _windowResize(self, event) -> None:
        """Metoda zjistí výšku a šířku framu calendarTable."""
        parent_width = event.width
        # unbind, rozpojí event, protože teď se bude konfigurovat obsah, takže by se stala nekonečná smyčka
        self.unbind('<Configure>')
        # nastavení velikosti frame podle resizování rodičovského okna
        if self.day_frames: # nastaví se jen pokud obsah existuje
            for frame in self.day_frames:
                frame.configure(width = ((parent_width/9)), height = (parent_width/9))
        # bind, opětovné zapnutí eventu
        self.bind('<Configure>', self._windowResize)

        #TODO vubec to nefunguje