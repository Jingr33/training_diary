#importy knihovan
from tkinter import *
import customtkinter as ctk
# importy souborů
from ctkWidgets import Frame, Button
from sports.setSport import SetSport


class SportDetailsFrame (Frame):
    def __init__(self, master :ctk.CTkBaseClass, option : str):
        super().__init__(master)
        self.master = master
        self.option = option # zároveň je to i název vybraného sportu

        # vytvoří grfafické rozhraní framu
        SetSport.plan_setSportDetails(self, self.option)
        # tlačítko pro přidání tréninku do kalendáře
        self._initAddButton()

    def getData(self) -> tuple:
        """Získá data ze zadaných údajů a uloží je jako plánovaný trénink."""
        # získání hodnot vstupů
        values = SetSport.plan_getSportDetails(self, self.option)
        return values
    
    def _initAddButton(self) -> None:
        """Vytvoření tlačítka pro přidání sportu do náhledového kalendáře."""
        self.add_button = Button(self, "Přidat", self.master.addTrainingToCalendar)
        self.add_button.pack(side = TOP, pady = 5)
        self.add_button.configure(anchor='center', width=95)

    def errorAnimation (self) -> None:
        """Vytvoří efekt animace tlačítka při zadání špatných vstupních údajů."""
        self.animation_time = 2000 # animacni cas v ms
        self.time = 0 # uběhnutý čas animace
        self.dt = 80 # časový úsek po který značí jeden snímek animace
        # barva "dodgerblue3 má rgb (24, 116, 205)"
        rgb_danger_red = [232, 12, 23]
        self.add_button.configure(text = "Špatné zadání", fg_color = self._rgbToHex(rgb_danger_red), hover = False)
        self._errorAfter(rgb_danger_red) 

    def _errorAfter(self, rgb : list) -> None:
        """After funce pro volání sebe samotné po dobu animace tlačítka přidat."""
        if self.time <= self.animation_time/2: # podmínka to kdy se s tlačítkem ještě nic neděje
            self.add_button.after(self.dt, lambda: self._errorAfter(rgb))
        elif self.time <= self.animation_time: # tady se tlačítko přeměňuje
            rgb[0] = rgb[0] - 16
            rgb[1] = rgb[1] + 8
            rgb[2] = rgb[2] + 14
            self.add_button.configure(fg_color = self._rgbToHex(rgb), hover = False, text = "Přidat")
            self.add_button.after(self.dt, lambda: self._errorAfter(rgb))
        else: # tady se fce ukončí
            self.add_button.configure(hover = True)
        self.time = self.time + self.dt
        return

    def _rgbToHex(self, rgb):
        """Převod barvy zadané v rgb do barvy v hex.""" # protože tkinter neumí rgb
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'
