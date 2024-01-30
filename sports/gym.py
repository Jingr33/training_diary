#importy knihovan
import customtkinter as ctk
from tkinter import *
#importy souborů
from sports.sport import Sport
from configuration import sport_list, sport_color, gym_body_parts
from ctkWidgets import Label, Entry, CheckBox

class Gym (Sport):
    """Třída pro funkce, které jsou specifické pro trénink typu posilovna."""
    def __init__(self):
        super().__init__()
        self.name = sport_list[0]
        self.color = sport_color[self.name]

    def createAttributes(self, training : object) -> list:
        self.message_attributes = ["datum", "sport", "čas", "cviky"]
        return self.message_attributes

    def createValues(self, training : object) -> list:
        """Metoda vytvoří list  atributů pro vepsání do tooltip message."""
        str_time  = str(training.time) + " min"
        self.message_values = [training.date, training.sport, str_time, training.practicedParts]
        return self.message_values
    
    @staticmethod
    def plan_initRunDetails (master : object) -> None:
        """Vytvoří widgety v framíku v detailech nastavování sportu (posilovna) ve vytváření
        cyklického tréninkového plánu."""
        # stringvar promenne pro ukládání zadaných dat
        master.estimated_time = StringVar()
        master.estim_leg = StringVar(value=0)
        master.estim_core = StringVar(value=0)
        master.estim_breast = StringVar(value=0)
        master.estim_shoulder = StringVar(value=0)
        master.estim_back = StringVar(value=0)
        master.estim_biceps = StringVar(value=0)
        master.estim_triceps = StringVar(value=0)
        master.estim_forearm = StringVar(value=0)

        # očekáváný strávený čas
        time_l = Label(master, "Očekávaný čas:")
        time_l.pack(side=TOP)
        time_l.configure(width = 95, anchor = 'w')

        time_e = Entry(master, master.estimated_time)
        time_e.pack(side=TOP)
        time_e.configure(width=95)

        # očekávané odvičené části těla
        parts_l = Label(master, "Cviky:")
        parts_l.pack(side=TOP)
        parts_l.configure(width=95, anchor='w')

        leg_chb = CheckBox(master, gym_body_parts[0], master.estim_leg)
        leg_chb.pack(side = TOP, pady=1)
        leg_chb.configure(width=95)

        core_chb = CheckBox(master, gym_body_parts[1], master.estim_core)
        core_chb.pack(side = TOP, pady=1)
        core_chb.configure(width=95)

        breast_chb = CheckBox(master, gym_body_parts[2], master.estim_breast)
        breast_chb.pack(side = TOP, pady=1)
        breast_chb.configure(width=95)

        shoulder_chb = CheckBox(master, gym_body_parts[3], master.estim_shoulder)
        shoulder_chb.pack(side = TOP, pady=1)
        shoulder_chb.configure(width=95)

        back_chb = CheckBox(master, gym_body_parts[4], master.estim_back)
        back_chb.pack(side = TOP, pady=1)
        back_chb.configure(width=95)

        biceps_chb = CheckBox(master, gym_body_parts[5], master.estim_biceps)
        biceps_chb.pack(side = TOP, pady=1)
        biceps_chb.configure(width=95)

        triceps_chb = CheckBox(master, gym_body_parts[6], master.estim_triceps)
        triceps_chb.pack(side = TOP, pady=1)
        triceps_chb.configure(width=95)

        forearm_chb = CheckBox(master, gym_body_parts[7], master.estim_forearm)
        forearm_chb.pack(side = TOP, pady=1)
        forearm_chb.configure(width=95)


    @staticmethod
    def plan_getRunDetails (master : object) -> tuple:
        """Vrátí data vložené do framíku sportu (běh) v nastavování cyklického tréninkového plánu 
        -> nastavení detailů sportu"""
        time = Sport.floatEntryChecker(master.estimated_time.get()) # kontrola vstupu času
        
        # list získaných hodnot z chceckboxů
        values_list = [master.estim_leg.get(), master.estim_core.get(), master.estim_breast.get(),
                master.estim_shoulder.get(), master.estim_back.get(), master.estim_biceps.get(),
                master.estim_triceps.get(), master.estim_forearm.get()]
        chceckbox_list = Sport.emptyCheckboxChecker(values_list) # kontrola zadání dat do chceckboxů
        return (time, chceckbox_list)
