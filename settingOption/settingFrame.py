# import knihoven
from tkinter import *
import customtkinter as ctk
from icecream import ic
# import souborů
from settingOption.sportSelectionFrame import SportSelectionFrame
from settingOption.plansOverview.plansOverviewWindow import PlansOverviewWindow
from ctkWidgets import Frame, Label, Entry, Switch, Button
from general import General
from configuration import colors
import globalVariables as GV

class SettingFrame (Frame):
    """Načte frame s widgetami pro manuální nastavení různých funkcí aplikace."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.side_pad = 15
        self.columnconfigure([0, 1], weight = 0)
        self.rowconfigure([0,1,2,3,4,6,7, 8, 9], weight = 1)
        self._initGUI()

    def _initGUI (self) -> None:
        """Vytvoření widgetů ve framu."""
        #nadpis
        title_pad = 6
        title = Label(self, "Nastavení", ("Arial", 17))
        title.grid(row = 0, column = 0, sticky = ctk.W, columnspan = 2, padx = (self.side_pad, title_pad), pady = title_pad)
        title.configure(text_color = colors["light"])
        # jednotlivé nastavení
        self.name_font = ("Arial", 14, 'bold')
        self.bottom_pad = (0, 25)
        self._fullscreenSwitcher()
        self._plansOverview()
        self._sportSelection()
        self._rowsInOverview()

    def _fullscreenSwitcher (self) -> None:
        """Vytvoří widgety s nastavení zapínání okna na fullscreen při spuštění."""
        option_name = Label(self, "Celá obrazovka", self.name_font)
        option_name.grid(row = 1, column = 0, sticky = ctk.W, padx = self.side_pad)
        self.switch_value = IntVar()
        self.switch_value.set(GV.getAutoFullscreen())
        switcher = Switch(self, "", self._setAutoFullscreen, self.switch_value)
        switcher.grid(row = 1, column = 1, padx = (0, self.side_pad))
        description = Label(self, "Při spuštění zobrazí aplikaci na celou obrazovku.")
        description.grid(row = 2, column = 0, columnspan = 2, sticky = ctk.W, pady = self.bottom_pad, padx = self.side_pad)

    def _plansOverview (self) -> None:
        """Vytvoří widgety s přehledem naastavených tréninkových plánu (a možnostmi mazání)."""
        option_name = Label(self, "Tréninkové plány", self.name_font)
        option_name.grid(row = 3, column = 0, sticky = ctk.W, padx = self.side_pad)
        plan_button = Button(self, "Přehled", self._openPlansOverview)
        plan_button.grid(row = 3, column = 1, padx = (0, self.side_pad))
        plan_button.configure(width = 130)
        description = Label(self, "Zobrazí přehled tréninkových plánu. Umožňuje jejich mazání.")
        description.grid(row = 4, column = 0, sticky = ctk.W, columnspan = 2, padx = self.side_pad, pady = self.bottom_pad)

    def _sportSelection (self) -> None:
        """Vytvoří widgety s výběrem přidání nebo odebrání sportu a možností zvolit si barvu pro daný sport (nebo nechat defaultní)."""
        option_name = Label(self, "Sporty", self.name_font)
        option_name.grid(row = 5, column = 0, sticky = "NW", padx = self.side_pad)
        option_name.configure(height = 35)
        sport_selection = SportSelectionFrame(self)
        sport_selection.grid(row = 7, column = 0, columnspan = 2, sticky = "NSWE", padx = (20, self.side_pad), pady = self.bottom_pad)
        description = Label(self, "Přidání či odebrání odtrénovaných sportů a nastavení jejich barvy v aplikaci.")
        description.grid(row = 6, column = 0, sticky = "NW", padx = self.side_pad)

    def _rowsInOverview (self) -> None:
        """Vytvoří widgety pro nastavení počtu řádků zobrazovaných v overview (na jednu stránku)."""
        option_name = Label(self, "Položek na stránce", self.name_font)
        option_name.grid(row = 8, column = 0, sticky = ctk.W, padx = self.side_pad)
        self.var_rows = StringVar()
        self.var_rows.set(GV.setting["overview-rows"])
        self.rows_entry = Entry(self, self.var_rows)
        self.rows_entry.grid(row = 8, column = 1, padx = (0, self.side_pad))
        self.rows_entry.configure(width = 130)
        self.rows_entry.bind("<KeyRelease>", self._setRowsInOverview)
        description = Label(self, "Počet řádků zobrazovaných na stránce přehledu tréninků.")
        description.grid(row = 9, column = 0, columnspan = 2, sticky = ctk.W, padx = self.side_pad, pady = self.bottom_pad)

    def _setAutoFullscreen (self) -> None:
        """Uloží nově nastavenou hodnotu nastavení velikosti okna při zapnutí aplikace."""
        GV.setting["auto-fullscreen"] = self.switch_value.get()
        GV.overwriteSettingFile()

    def _openPlansOverview (self) -> None:
        """Otevře přehled tréninkových plánu v nastavení aplikace."""
        PlansOverviewWindow(self)

    def _setRowsInOverview (self, value) -> None:
        """Zkontroluje vstup a uloží nastavení počtu řádků zobrazovaných v přehledu tréninků na jednu stránku."""
        entry = self.var_rows.get()
        if General.checkIntEntry(entry) and General.checkGreater0(float(entry)): # kontrola vstupu
            GV.setting["overview-rows"] = entry
            GV.overwriteSettingFile()
            General.setDefaultBorder(self.rows_entry)
        else:
            General.setRedBorder(self.rows_entry)