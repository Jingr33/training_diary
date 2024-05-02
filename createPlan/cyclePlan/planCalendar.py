#importy knihoven
from tkinter import *
import customtkinter as ctk
#importy souborů
from createPlan.cyclePlan.oneDay import OneDay
from ctkWidgets import Label, Button


class PlanCalendar (ctk.CTkScrollableFrame):
    """Vytvoří malý náhled kalendáře v nastavovacím okné cyklického tréninkového plánu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.column = 0
        self.columns = []
        self.next_day_button = 0
        # list s widgettami pro kazdy den
        self.days = []
        #nastavení řádků
        self.rowconfigure([0, 1], weight=1)
        # inicializace grafického rozhraní
        self._createGUI()

    def _createGUI(self) -> None:
        """Vytvoření grafického rozhraní nastavení."""
        self.calendar_label = Label(self, "Nastavení tréninkového cyklu:", ("Arial", 15, 'bold'))
        self.calendar_label.grid(row=0, column=0, sticky='w', columnspan=2)
        # přidání prvního dne
        self._addDay()

    def _addDay(self) -> None:
        """Přidání dalšího dne v náhledovém kalendáři."""
        # zrušení tlačítka next_day_button na původním místě
        if self.next_day_button:
            self.next_day_button.destroy()
        # vytvoření objektu s widgetami pro jeden den
        self.day_number = len(self.columns)+1
        one_day = OneDay(self, self.day_number)
        one_day.grid(row=1, column = self.column, sticky = "NW")
        one_day.configure(fg_color = "transparent", corner_radius=0)
        # tlačítko pro přidání dalšího dne
        self._nextDayButton()
        # nastavení columnspan labelu nadpisu
        self.calendar_label.grid(row=0, column=0, sticky='w', columnspan=self.column+1)
        # nastavení sloupců
        self.columns.append(self.column)
        self._columnsSetting()
        # zvětšení proměnné sloupec
        self.column = self.column + 1
        # přidání widgetů do listu
        self.days.append(one_day)
        # ošetření podmínky posledního sloupce
        self._lastColumnException()

    def _nextDayButton(self) -> None:
        """Vytvoření tlačítka pro přidání dalšího dne"""
        self.next_day_button = Button(self, "Přidat den", self._addDay)
        self.next_day_button.grid(row=1, column=self.column+1, sticky='NW', pady = 40)
        self.next_day_button.configure(width=80, height = 30)

    def _removeFrame(self, frame_number : int) -> None:
        """Odstraní frame dne i celý jeho sloupec z náhledu kalendáře."""
        # vymazání požadovaného dne
        self.days[frame_number].destroy()
        del self.days[frame_number]
        # přepsání labelů do pořádku
        self._dayReindexation()
        # odebere se sloupec
        del self.columns[-1]
        # nastavení sloupců
        self._columnsSetting()
        # pokud zbývá poslední den, nelze odebrat
        self._lastColumnException()
    
    def _columnsSetting (self) -> None:
        """Nastavuje vlastnosti sloupců v mřížce podle počtu dní."""
        if len(self.columns) >= 6:
            self.columnconfigure(self.columns, weight=1)
        else:
            self.columnconfigure(self.columns, weight=0)

    def _dayReindexation (self) -> None:
        """Přepíše data dnů na správná."""
        i = 1
        for one_day in self.days:
            if one_day != None:
                one_day.day_number = i
                one_day.frame_number = i - 1
                one_day.dayRindexation()
                i = i + 1

    def _lastColumnException (self) -> None:
        """Pokud plán tvoří jen jeden den, tlačítko pro odstranění bude disabled."""
        # pokud zbyde poslední den, jeho odebrání se znemožní
        if len(self.columns) == 1:
            for day in self.days:
                if day != None:
                    day.remove_button.configure(state = "disabled")
        # pokud jsou zobrazeny alespoň 2 dny, možnost odstranění se zpřístupní
        elif len(self.columns) == 2:
            for day in self.days:
                if day != None:
                    day.remove_button.configure(state = "enabled")