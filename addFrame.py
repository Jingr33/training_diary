# import knihoven
import customtkinter as ctk
from tkinter import *
# importy souborů
from ctkWidgets import Button
from ctkWidgets import Label
from ctkWidgets import ComboBox
from setFrame import Frame as SetFrame


class Frame (ctk.CTkFrame):
    """Třída vytvářející frame v hlavním okně pro přidávání aktivit."""
    def __init__(self, master:ctk.CTkBaseClass) -> None:
        super().__init__(master)

        # pole s možnými sporty na výběr
        self.options = ["běh", "posilovna"]

        # inicializace proměnné pro setFrame a nastavení na 0
        self.setFrame = 0

        self.gui()

    def gui(self):
        """Metoda pro incializaci widgetů v addframu."""

        # tlačítko pro tréninkový plán
        button_plan = Button(self, 'Nastavit plán', self.hello)
        button_plan.pack(padx=30, pady=10, ipadx=10, ipady=8, side=TOP)

        # Přidání nového tréninku
        new_training_l = Label(self, 'Nový trénink', ("Arial", 20))
        new_training_l.pack(pady=15, side=TOP)

        # widgety s vyběrem aktivity
        activity_l = Label(self, 'Aktivita')
        activity_l.pack(side=TOP, anchor=ctk.W, padx=10)
        activity_cb = ComboBox(self, self.options, self.show_frame, "posilovna")
        activity_cb.pack(side=TOP, anchor=ctk.W, padx=10)
        activity_cb.set("nevybráno")


    def show_frame(self, choice):
        """inicializace dynamicky se měnícího framu nastavování podle vybraního sportu"""
        
        # vymazání předchozího framu
        if self.setFrame:
            self.setFrame.destroy()

        # inicializace framu vybraného sportu
        self.setFrame = SetFrame(self, choice)
        self.setFrame.pack(side=TOP, padx=3, pady=5, fill=ctk.BOTH, expand=TRUE)

######################################
    def hello(self):
        print("hello")
