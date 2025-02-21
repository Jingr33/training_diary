#importy knihoven
import customtkinter as ctk
from tkinter import *
# importy souborů
from calendarOption.calendarTable import calendarTable
from calendarOption.setMonthCalendar import SetMonth


class Calendar (ctk.CTkFrame):
    """Třída pro vytvoření záložky s kalendářem."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        # přidat posunovací popojíždění v kalendáři
        self.slider_frame = SetMonth(self)
        self.slider_frame.pack()
        self.slider_frame.configure(fg_color = "transparent")
        # aktuální datum
        self.current_date = self.slider_frame.setted_date
        # inicializace grafického kalendáře
        self.initCalTable(self.current_date)

    def initCalTable (self, date :tuple) -> None:
        """Provede inicializaci kalendáře."""  
        # kalendář - frame obsahující čtvercovou soustavu framů
        self.calendar_table = 0
        if self.calendar_table:
            self.calendar_table.destroy() # zrušení starého framu
        # nový kalendář
        self.calendar_table = calendarTable(self, date)
        self.calendar_table.pack(fill = ctk.BOTH, expand = True)
