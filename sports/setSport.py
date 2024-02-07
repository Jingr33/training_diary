# importy souborů
from sports.sport import Sport
from sports.gym import Gym
from sports.run import Run
from configuration import sport_list

class SetSport():
    """Třída pro nastavení základních vlastností pro jednotlivé sporty."""
    def createTooltipMessage(self, training : object) -> str:
        """Metoda určí, o který sport se jedná a pomocí dalších objektů vytvoří tooltip message."""
        if training.sport == sport_list[0]: # posilovna
            sport = Gym()
            attributes = sport.createAttributes(training)
            values = sport.createValues(training)
            message = sport.tooltipMessage()
        elif training.sport == sport_list[1]: # běh
            sport = Run()
            values = sport.createValues(training)
            attributes = sport.createAttributes(training)
            message = sport.tooltipMessage()
        else:
            ... #TODO další sporty
        return message

    @staticmethod
    def sortEachTrainingDict (master : object, training_dict : dict, key : str) -> list:
        """Vezme vložený slovník a rozhodne, zda a jakým způsobem se tento list třídí, 
        vrátí setříděný list tréninků.
        Vstup: 1) slovník s listy rozdělených tréninků,)
               2) klíč sportu, který se má setřídít."""
        # rozhodnutí o který sport se jedná
        if key == sport_list[0]: # posilovna
            training_dict[key] = Gym.sortGymTrainingList(master, training_dict[key])
        elif key == sport_list[1]: # běh
            training_dict[key] = Run.sortRunTrainingList(master, training_dict[key])
        else:
            ... #TODO
        return training_dict[key]
        