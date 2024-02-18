#import knihoven
from tkinter import *
import customtkinter as ctk
from datetime import date
# import souborů
from configuration import free_day

class OneFreeDay ():
    """Vytvoří aktivitu volného dne a připraví ho jako widgetu (label) do kalendáře."""
    def __init__(self,  date : date):
        self.real_date = date
        self.sport = free_day
