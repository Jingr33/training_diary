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
    
    def getOneSportTrainings (self, trainings : list, sport_name : str,
                               first_date : date, last_date : date) -> list:
        """Vrátí tréninky naležící pouze jednomu sportu v časovém rozmezí."""
        # rozhodnutí, který typ grafu se vykreslí
        chart_type, strings = SetSport.chooseChartType(sport_name)
        # vybere tréninky v termínu
        if chart_type == "pie":
            in_term_trains = self.getTrainingsInDate(trainings, first_date, last_date)
            one_sport = self._sortOneSport(in_term_trains, sport_name)
        elif chart_type == "bar":
            periods = self._otherColumnsDates(first_date, last_date)
            one_sport = []
            for period in periods:
                in_term_trains = self.getTrainingsInDate(trainings, period[0], period[1])
                one_sport_period = self._sortOneSport(in_term_trains, sport_name)
                one_sport.append(one_sport_period)
        return one_sport
    
    def _sortOneSport (self, term_trains : list, sport_name : str) -> list:
        """Z listu tréninků vybere tréninky pouze jednoho sportu."""
        one_sport = []
        for training in term_trains:
            if training.sport == sport_name:
                one_sport.append(training)
        return one_sport
    
    def _otherColumnsDates (self, first_date : date, last_date : date) -> list:
        """Vrátí list tuplů počettečního a koncového data pro každý sloupec grafu."""
        periods = [None] * 7
        delta = last_date - first_date
        for i in range(-3, 4):
            start_date = General.surroundingFirstDate(first_date, i*0, i*0, i*delta.days)
            end_date = General.surroundingLastDate(start_date, 0, 0, delta.days)
            periods[i + 3] = (start_date, end_date)
        return periods
