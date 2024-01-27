#importy knihovan
from tkinter import *
import customtkinter as ctk
# importy souborů
from ctkWidgets import Frame
from sports.setSport import SetSport


class SportDetailsFrame (Frame):
    def __init__(self, master :ctk.CTkBaseClass, option : str):
        super().__init__(master)
        self.master = master
        self.option = option # zároveň je to i název vybraného sportu

        # vytvoří grfafické rozhraní framu
        SetSport.plan_setSportDetails(self, self.option)

        self.bind('<Button-1>', self.getData)

    def getData(self, event) -> tuple:
        """Získá data ze zadaných údajů a uloží je jako plánovaný trénink."""
        values = SetSport.plan_getSportDetails(self, self.option)
        print(values)
        return values