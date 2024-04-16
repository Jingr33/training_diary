# import knihoven
import customtkinter as ctk
from tkinter import *
# import souborů
from overviewOption.overviewOption import Overview
from calendarOption.calendarOption import Calendar
from statisticsOption.StatisticsOption import Statistics
from settingOption.settingOption import Setting
from landingPage.landingPage import LandingPage 


class Frame (ctk.CTkFrame):
    """Obsahový frame - vybírá který vnitřní frame se zobrazí dále."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.configure(fg_color = "transparent")
        
    def overviewOption(self) -> None:
        """Metoda pro zavolání možností pro záložku přehled."""
        overview = Overview(self)
        overview.pack(fill = ctk.BOTH, expand=True)

    def calendarOption(self) -> None:
        """Metoda pro zavolání záložky Kalendář."""
        calendar = Calendar(self)
        calendar.pack(fill = ctk.BOTH, expand = True)

    def statisticsOption(self) -> None:
        """Metoda pro zavolání záložky Statistiky."""
        statistics = Statistics(self)
        statistics.pack(fill = ctk.BOTH, expand = True)

    def settingOption (self) -> None:
        """Metoda pro zavolání záložky Možnosti."""
        setting = Setting(self)
        setting.pack(fill = ctk.BOTH, expand = True)

    def landingPage (self) -> None:
        """?etoda pro vytvoření landing page při spuštění aplikace."""
        landing_page = LandingPage(self)
        landing_page.pack(fill = ctk.BOTH, expand = True)