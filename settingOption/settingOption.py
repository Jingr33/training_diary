# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from settingOption.personalDataFrame import PersonalDataFrame
from settingOption.settingFrame import SettingFrame
from configuration import colors


class Setting (ctk.CTkScrollableFrame):
    """Načte frame při zvolení "Možnosti" v horním baneru."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.configure(corner_radius = 8)
        self._initGUI()

    def _initGUI (self) -> None:
        """Vytvoří grafické rozhraní sekce nastavení."""
        pad = 3
        ipad = 6
        cor_rad = 8
        personal_data = PersonalDataFrame(self)
        personal_data.pack(side = TOP, fill = ctk.X, padx = pad, pady = pad, ipadx = ipad, ipady = ipad)
        personal_data.configure(corner_radius = cor_rad, fg_color = colors["dark-gray-3"])
        setting = SettingFrame(self)
        setting.pack(side = TOP, fill = ctk.X, padx = pad, pady = pad, ipadx = ipad, ipady = ipad)
        setting.configure(corner_radius = cor_rad, fg_color = colors["dark-gray-3"])