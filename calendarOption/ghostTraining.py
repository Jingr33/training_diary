#import knihoven
from datetime import date, timedelta
#import souborů
from configuration import free_day
from oneTraining import OneTraining


class GhostTraining ():
    """Třída vygeneruje smyšlené (plánované tréninky) v tréninkovém plánu ve zobrazované části."""
    def __init__ (self, plan : object, first_cycle : int, last_cycle : int):
        self.ghost_trainings = []
        # nastavení slovníku s začátečními daty cyklů
        self.next_cycle_date = plan.next_cycle
        # nastavení list tréninků a listu volných dní
        self._trainingOrFreeDay(plan)
        # vytvoření list smyšlených tréninků
        self.ghost_trainings = self._createGhostTrainsList(first_cycle, last_cycle)


    def getGhostTrainList (self) -> list:
        """Vrátí list smýšlených tréninků z tréninkoého plánu."""
        return self.ghost_trainings

    def _getFreeDaysList (self) -> list:
        """Vrátí list smyšlených volných dní z tréninkového plánu."""
        ...

    def _trainingOrFreeDay (self, plan) -> None:
        """Nastaví jako vlstnost list tréninků a list volných dní v tréninkovém plánu."""
        self.planned_trainings = []
        self.planned_free_days = []
        for activity in plan.activities:
            if activity.sport == free_day:
                self.planned_free_days.append(activity)
            else:
                self.planned_trainings.append(activity)

    def _createGhostTrainsList (self, first_cycle : int, last_cycle : int) -> list:
        """Vytvoří list tréninků naplanovaných v zobrazeném období v kalendáři."""
        trainings = []
        # cyklus přes období, ve kterém se vytváří tréninky
        for i in range(first_cycle, last_cycle):
            # cyklus přes trénikńky v plánu
            for training in self.planned_trainings:
                day_shift = training.day
                date = self.next_cycle_date[i] + timedelta(days = day_shift) # vytvoření data tréninku
                ghost_training = training # trénink z plánu se zkkopíruje do ghosta
                one_training = OneTraining() # instance one_training
                one_training.setGhostDate(ghost_training, date) # funkce nastaví tréninku datum
                trainings.append(ghost_training)
        return trainings