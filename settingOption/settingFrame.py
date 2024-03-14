# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů


class SettingFrame (Frame):
    """Načte frame s widgetami pro manuální nastavení různých funkcí aplikace."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master