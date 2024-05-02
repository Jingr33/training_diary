# import knihoven
from tkinter import *
from icecream import ic
# import osuborů
from oneTraining import OneTraining
from general import General


class OneSingleTraining ():
    """Třída pro zpracování dat jednoho tréninkového plánu z databáze jednoduchých tréninkových plánů."""
    def __init__(self, plan_data : list):
        # plan_data = self._dataLineToList(plan_data)
        self.dates = self._getTrainTerms(plan_data[0])
        # self._getTrainingInfo(plan_data[1]) # nastaví jako vlastnosti
        self.all_trainings = self._createTrainings(plan_data[1])
        # získání seřazených dat, prvního a posledního data, kdy se uskuteční nějaký trénink z plánu
        self.sorted_dates = self._sortTerms()
        self.start_date, self.end_date = General.getBorderTerms(self.sorted_dates)

    def _getTrainTerms (self, date_data : str) -> list:
        """Přetvoří string dat získaných z databáze na proměnné typu datetime a vrátí list dat."""
        date_data = General.separateData(date_data) # vytvoření dat ve formě stringů
        del date_data[-1]
        return date_data

    def _createTrainings (self, trainings_str : str) -> list:
        """Vytvoří list všech tréninků, které tréninkový plán obashuje (pomocí třídy OneTraining)."""
        all_trains = [None] * len(self.dates)
        for i in range(len(self.dates)):
            data_line = "{0} / {1}".format(self.dates[i], trainings_str)
            new_training = OneTraining(self, "load_single_plan", data_line)
            all_trains[i] = new_training
        return all_trains
    
    def _sortTerms (self) -> list:
        """Seřadí data tréninků od nejstaršího po nejnovější, vrátí list dat ve formátu date."""
        for i in range(len(self.dates)):
            self.dates[i] = General.stringToDate(self.dates[i]) # na formát date
        self.dates.sort()
        return self.dates