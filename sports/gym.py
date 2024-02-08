#importy knihovan
import customtkinter as ctk
from tkinter import *
#importy souborů
from sports.sport import Sport
from configuration import sport_list, sport_color, gym_body_parts, unknown_text
from ctkWidgets import Label, Entry, CheckBox
from general import General

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
    def sortGymTrainingList (master : object, training_list : list) -> list:
        """Roztřídí skupinu tréninků posilovna."""
        # akorát, že posilovna se nijak netřídí...zatím
        return training_list
    
    @staticmethod
    def plan_initGymDetails (master : object) -> None:
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
    def plan_getGymDetails (master : object) -> tuple:
        """Vrátí data vložené do framíku sportu (běh) v nastavování cyklického tréninkového plánu 
        -> nastavení detailů sportu"""
        time = Sport.floatEntryChecker(master.estimated_time.get()) # kontrola vstupu času
        
        # list získaných hodnot z chceckboxů
        values_list = [master.estim_leg.get(), master.estim_core.get(), master.estim_breast.get(),
                master.estim_shoulder.get(), master.estim_back.get(), master.estim_biceps.get(),
                master.estim_triceps.get(), master.estim_forearm.get()]
        chceckbox_list = Sport.emptyCheckboxChecker(values_list) # kontrola zadání dat do chceckboxů
        return (time, chceckbox_list)

    @staticmethod
    def gymData(master : object, data_list : list, index_adjustment = 2) -> None:
        """Rozklíčuje data z získané z tréninkové databáze pokud se
        jedná o trénink posilovna.
        Index_adjustment je úprava indexu, pokud tam chci poslat pole kde ty atributy neberu od 0."""
        master.time = General.checkIntEntry(data_list[0 + index_adjustment])
        # zklouška, zda bylo něco zadáno
        if data_list[1 + index_adjustment] != unknown_text:
            master.leg = int(data_list[1 + index_adjustment])
            master.core = int(data_list[2 + index_adjustment])
            master.breast = int(data_list[3 + index_adjustment])
            master.shoulders = int(data_list[4 + index_adjustment])
            master.back = int(data_list[5 + index_adjustment])
            master.biceps = int(data_list[6 + index_adjustment])
            master.triceps = int(data_list[7 + index_adjustment])
            master.forearm = int(data_list[8 + index_adjustment])
            # vytvoření vlastnosti practicedParts
            master.practicedParts = Gym.practicedPartsString(master)
        else:
            master.practicedParts = unknown_text

    @staticmethod
    def practicedPartsString (master : object):
        "Vytvoří string procvčených částí těla."
        # pole částí těla
        parts = [master.leg, master.core, master.breast, master.shoulders, master.back,
                 master.biceps, master.triceps, master.forearm]
        # vytvoření slovního podání odcvičených částí těla
        practiced_parts = ""
        text = ""
        i = 0
        for part in parts: # přes věechny možné odcvičené části těla
            if part == 1: # pokud byla odcvičena
                if practiced_parts != "": #udělá se mezery mezi slovy
                    text = ", "
                text = text + gym_body_parts[i]
                practiced_parts = practiced_parts + text
            i = i + 1
        return practiced_parts

    @staticmethod
    def plan_getGymData (master : object, data : tuple) -> None:
        """Přiřadí zadané data tréninku typu posilovna."""
        data_list = data[1]
        # vyhodnocení, zda je v listu něco zadáno
        data_check = Gym.tryGymData(data_list)
        # uložení dat
        if data_check:
            master.leg = int(data_list[0])
            master.core = int(data_list[1])
            master.breast = int(data_list[2])
            master.shoulders = int(data_list[3])
            master.back = int(data_list[4])
            master.biceps = int(data_list[5])
            master.triceps = int(data_list[6])
            master.forearm = int(data_list[7])
            # vytvoření vlastnosti practicedParts
            master.practicedParts = Gym.practicedPartsString(master)
        else:
            master.practicedParts = unknown_text

    @staticmethod
    def tryGymData (data_list : list) -> bool:
        """Vyhodnotí, zda je v listu jakákoliv zadaná hodnota -> True, jinak False."""
        try:
            int(data_list[2])
            check = True
        except:
            check = False
        return check
    
    @staticmethod
    def plan_gymDataToList(training : object) -> list:
        """Zapíše vlastnosti tréninku posilovna do listu."""
        # podmínka pro prázné data
        if training.practicedParts == unknown_text:
            data_list = [training.date, training.sport, training.time, unknown_text]
        else:
            # vytvoření listu
            data_list = [training.date, training.sport, training.time, training.leg, training.core, training.breast,
                        training.shoulders, training.back, training.biceps, training.triceps,
                        training.forearm]
        return data_list
