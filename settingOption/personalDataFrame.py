# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů


class PersonalDataFrame (Frame):
    """Načte frame s nastavením osobních údajů."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master