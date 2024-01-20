# import knihoven
import customtkinter as ctk
from tkinter import *
# import souborů
from overviewOption.overviewOption import Overview
from calendarOption.calendarOption import Calendar

class Frame (ctk.CTkFrame):
    """Obsahový frame - vybírá který vnitřní frame se zobrazí dále."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        
    def overviewOption(self) -> None:
        """Metoda pro zavolání možností pro záložku přehled."""
        # vytvoření instace s přehledem tréninků.
        overview = Overview(self)
        overview.pack(fill = ctk.BOTH, expand=True)

    def calendarOption(self) -> None:
        """Metoda pro zavolání záložky Kalendář."""
        calendar = Calendar(self)
        calendar.pack(fill = ctk.BOTH, expand = True)