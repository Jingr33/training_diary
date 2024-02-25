# importy knihoven
from tkinter import *
import customtkinter as ctk
from CTkToolTip import *
from pywinstyles import set_opacity
# importy souborů
from ctkWidgets import Label
from sports.setSport import SetSport
from configuration import sport_color

class OneStrip (Label):
    """Objekt tvořící strip v kalendáři a na něm se zobrazující tooltip."""
    def __init__(self, master :ctk.CTkBaseClass, training : object, font : tuple):
        super().__init__(master, training.sport, font)

        self._labelColor(training)

        self.message = SetSport().createTooltipMessage(training)

        CTkToolTip(self, delay=0.2, message=self.message, justify = 'left', 
                   alpha = 0.8, x_offset= -50, y_offset=-100)

    def _labelColor (self, training : object) -> None:
        """Nastaví barvu pozadí labelu."""
        if hasattr(training, "ghost"):
            self.configure(fg_color = sport_color[training.sport])
            set_opacity(self, value = 0.3) # nastavení opacity pozadí labelu
        else:
            self.configure(fg_color = sport_color[training.sport])
