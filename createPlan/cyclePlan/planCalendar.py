#importy knihoven
from tkinter import *
import customtkinter as ctk
#importy souborů
from createPlan.cyclePlan.dayDetail import DayDetailFrame
from ctkWidgets import Label, Button
from configuration import colors

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
        # self.columnconfigure(0, weight = 1)
        self.rowconfigure([0, 1, 2], weight=1)

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
        one_day = []

        # zrušení tlačítka next_day_button na původním místě
        if self.next_day_button:
            self.next_day_button.destroy()

        # frame dne
        frame = DayDetailFrame(self, len(self.columns) + 1)
        frame.grid(row=1, column = self.column, padx=2, pady=2, ipadx=3, ipady=3, 
                   sticky='w')
        frame.configure(fg_color=colors["light-gray"], corner_radius = 10)
        one_day.append(frame)

        # odstranění dne
        day_number = len(self.days)
        remove_button = Button(self, "Odstranit", lambda: self._removeFrame(day_number))
        remove_button.grid(row=2, column=self.column, padx=2, pady=2, sticky='w')
        remove_button.configure(height = 13, width=115, font=("Arial", 11))
        one_day.append(remove_button)

        # podrobnosti nastavení

        # checkbox pro volný den

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
        self.next_day_button.grid(row=1, column=self.column+1, sticky='w')
        self.next_day_button.configure(width=80, height = 30)

    def _removeFrame(self, day_number : int) -> None:
        """Odstraní frame dne i celý jeho sloupec z náhledu kalendáře."""
        # vymazání widgetů požadovaného dne
        for widget in self.days[day_number]:
            widget.destroy()
        self.days[day_number] = None
        # self.days[day_number] = None
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
        for frame in self.days:
            if frame != None:
                frame[0].number_of_day = i
                frame[0].dayReindexation(str(i))
                i = i + 1

    def _lastColumnException (self) -> None:
        """pokud zbývá poslení den, tlačítko pro odstranění bude disabled."""
        # pokud zbyde poslední den, jeho odebrání se znemožní
        if len(self.columns) == 1:
            for day in self.days:
                if day != None:
                    day[1].configure(state = "disabled")
        # pokud jsou zobrazeny alespoň 2 dny, možnost odstranění se zpřístupní
        elif len(self.columns) == 2:
            for day in self.days:
                if day != None:
                    day[1].configure(state = "enabled")