#import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from overviewOption.updateTraining.updateFrame import UpdateFrame


class UpdateWindow (ctk.CTkToplevel):
    """Toplevel okno pro změnu v nastavení tréninku v overview tréninků."""
    def __init__ (self, master : ctk.CTkBaseClass, training : object):
        super().__init__(master)
        self.master = master
        self.training = training
        self.title_text = self._titleText()
        self.title(self.title_text)
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.kill)
        self.geometry("400x180")
        self.resizable(False, False)
        # frame
        self._initFrame()

    def _initFrame (self) -> None:
        """Vytvoří frame okna."""
        self.frame = UpdateFrame(self, self.training)
        self.frame.pack(fill = ctk.BOTH, expand = True, ipadx = 10, ipady = 10)

    def _titleText (self) -> str:
        """Vytvoří title okna."""
        sport = self.training.sport.upper()
        text = "Upravit trénink " + str(sport)
        return text

    def kill (self) -> None:
        """Zavření okna."""
        self.master.rowSettings()
        self.destroy()