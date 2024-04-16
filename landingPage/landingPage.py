# import knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from landingPage.infoFrame import InfoFrame
from ctkWidgets import Frame, Label
from configuration import colors

class LandingPage (Frame):
    """Třída generující widgety na landing page při spuštění aplikace."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self._initTitle()
        self._infoFrame()
        
    def _initTitle (self) -> None:
        """Vytvoří widget s nadpisem stránky."""
        title = Label(self, "Tréninkový deník", ("Arial", 23))
        title.pack(side = TOP, anchor = "w", padx = 20, pady = (20, 10))
        title.configure(text_color = colors["light"])

    def _infoFrame (self) -> None:
        """Vytvoří frame s doplňkovými informace landing page."""
        picture_frame = InfoFrame(self)
        picture_frame.pack(side = TOP, pady = (80, 30))