# import knihovem
from tkinter import *
import customtkinter as ctk
#import souborů
from configuration import legend
from ctkWidgets import Label
from configuration import colors

class Legend (ctk.CTkFrame):
    """Třída pro vytvoření framu s legendou."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        # nastavení barvy framu
        self.configure(fg_color = colors["dark-gray"])

        # vytvoření labelů s popisky
        date_l = Label(self, legend[0])
        date_l.pack(side=LEFT, fill = ctk.Y)
        date_l.configure(width=100, height=45, font=("Arial", 14, 'bold'))

        sport_l = Label(self, legend[1])
        sport_l.pack(side=LEFT, fill = ctk.Y)
        sport_l.configure(width=110, height=45, anchor=ctk.W, font=("Arial", 14, 'bold'))

        time_l = Label(self, legend[2])
        time_l.pack(side=LEFT, fill = ctk.Y)
        time_l.configure(width=70, height=45, anchor=ctk.W, font=("Arial", 14, 'bold'))

        details_l = Label(self, legend[3])
        details_l.pack(side=LEFT, fill = ctk.Y)
        details_l.configure(width=250, height=45, anchor=ctk.W, font=("Arial", 14, 'bold'))

