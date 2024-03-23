# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from landingPage.progressFrame import ProgressFrame
from ctkWidgets import Frame, Label
from configuration import colors

class LandingPage (Frame):
    """Třída generující widgety na landing page při spuštění aplikace."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self._initTitle()
        self._progressFrame()
        
    def _initTitle (self) -> None:
        """Vytvoří widget s nadpisem stránky."""
        title = Label(self, "Tréninkový deník", ("Arial", 28))
        title.pack(side = TOP, fill = ctk.X, anchor = "center", padx = 20, pady = (20, 10))
        title.configure(text_color = colors["light"])

    def _progressFrame (self) -> None:
        """Vytvoří frame s obrázkem a carousel texty."""
        picture_frame = ProgressFrame(self)
        picture_frame.pack(side = TOP, fill = ctk.X, padx = 10, pady = 15)