# importy knihoven
from tkinter import *
import customtkinter as ctk
from CTkToolTip import *
# importy souborů
from ctkWidgets import Label
from sports.setSport import SetSport

class OneStrip (Label):
    """Objekt tvořící strip v kalendáři a na něm se zobrazující tooltip."""
    def __init__(self, master :ctk.CTkBaseClass, training : object, font : tuple):
        super().__init__(master, training.sport, font)

        self.message = SetSport().createTooltipMessage(training)

        CTkToolTip(self, delay=0.2, message=self.message, justify = 'left', 
                   alpha = 0.8, x_offset= -50, y_offset=-100)

