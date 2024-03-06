# import knihoven
from tkinter import *
import customtkinter as ctk
from icecream import ic
# import osuborů
from oneTraining import OneTraining
from general import General


class OneSingleTraining ():
    """Tří da pro zpracování dat jednoho tréninkového plánu z databáze jednoduchých tréninkových plánů."""
    def __init__(self, plan_data : list):
        # plan_data = self._dataLineToList(plan_data)
        self.dates = self._getTrainTerms(plan_data[0])
        # self._getTrainingInfo(plan_data[1]) # nastaví jako vlastnosti
        self.all_trainings = self._createTrainings(plan_data[1])

    # def _dataLineToList (self, plan_data : list) -> list:
    #     """Převede informace z listu stringů řádků převzatých z databáze do list listů s oddělenými informacemi."""
    #     for i in range(len(plan_data)):
    #         plan_data[i] = General.separateData(i)
    #     return plan_data
    
    def _getTrainTerms (self, date_data : str) -> list:
        """Přetvoří string dat získaných z databáze na proměnné typu datetime a vrátí list dat."""
        date_data = General.separateData(date_data) # vytvoření dat ve formě stringů
        del date_data[-1]
        return date_data
    
    # def _getTrainingInfo (self, training_data : list) -> None:
    #     """Z listu informací o vlastnostech tréninku uloží informace jako vlastnosti       tréninkového plánu."""
    #     self.sport = training_data[0] # nastavení sportu
    #     SetSport.findData(self, training_data, 1) # nastavení podrobností sportu

    def _createTrainings (self, trainings_str : str) -> list:
        """Vytvoří list všech tréninků, které tréninkový plán obashuje (pomocí třídy OneTraining)."""
        all_trains = [None] * len(self.dates)
        for i in range(len(self.dates)):
            data_line = "{0} / {1}".format(self.dates[i], trainings_str)
            new_training = OneTraining(self, "load_single_plan", data_line)
            all_trains[i] = new_training
        return all_trains
    
######################################################################################
# celé blbě, ty funkce pro vytváření vlastností se stejně udělají ve OneTRainingu znovu, tak tam jenom nasypej ty řádky spojené pro každý jeden trénink a už nechej one_training si to nastavit, páč stejně pak ty vlastnosti usí mít OneTraining ne tohle.
#######################################################################################

        

