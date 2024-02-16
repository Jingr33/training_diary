#import knihoven
from datetime import date
# import souborů
from general import General
from configuration import trainings_path
from oneTraining import OneTraining
from sports.setSport import SetSport


class DataLoader ():
    """Získá data z databáze a upraví je dle potřeby grafu."""
    def __init__(self):
        data_lines = General.loadLinesFromFile(trainings_path)
        self.trainings = self._makeTrainings(data_lines)

    def _makeTrainings (self, data_lines : list) -> list:
        """Vrátí list objektů tréninků."""
        trainings = []
        for line in data_lines:
            training = OneTraining(self, "load", line)
            trainings.append(training)
        return trainings

    def getAllTrainings (self) -> list:
        """Vrátí list všech tréninků."""
        return self.trainings
    
    def getOneSportTrainings (self, sport : str) -> list:
        """Vrátí list tréninků, které patří zadanému sportu."""
        return SetSport.getOneSportTrainings(self, sport)
    
    def getTrainingsInDate (self, trainings : list, first_date : date, last_date : date) -> list:
        """Ze zadaných tréninků vybere tréninky uskutečněné mezi zadanými daty.
        Vrátí list tréninků."""
        trains_between = []
        for training in trainings:
            after_from_date = training.real_date >= first_date
            before_last_date = training.real_date <= last_date
            if after_from_date and before_last_date:
                trains_between.append(training)
        return trains_between
    