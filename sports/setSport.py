# importy souborů
from sports.sport import Sport
from sports.gym import Gym
from sports.run import Run
from configuration import sport_list

class SetSport():
    """Třída pro nastavení základních vlastností pro jednotlivé sporty."""
    def createTooltipMessage(self, training : object) -> str:
        """Metoda určí, o který sport se jedná a pomocí dalších objektů vytvoří tooltip message."""
        if training.sport == sport_list[0]:
            sport = Gym()
            attributes = sport.createAttributes(training)
            values = sport.createValues(training)
            message = sport.tooltipMessage()
        elif training.sport == sport_list[1]:
            sport = Run()
            values = sport.createValues(training)
            attributes = sport.createAttributes(training)
            message = sport.tooltipMessage()
        else:
            ... #TODO další sporty
        return message
    
    @staticmethod
    def plan_setSportDetails(master : object, option : str) -> None:
        """Rozhodne, které podrobnosti sportu ve tvoření cyklického tréninkového plánu
        se vytvoří a zavolá danou funkci z objektu daného sportu."""
        if option == sport_list[0]: # posilovna
            Gym.plan_initRunDetails(master)
        elif option == sport_list[1]: # běh
            Run.plan_initRunDetails(master)

    @staticmethod
    def plan_getSportDetails(master : object, option : str) -> tuple:
        """Rozhodne, ze kterého sportu data pochází a získá je."""
        if option == sport_list[0]: # posilovna
            values = Gym.plan_getRunDetails(master)
        elif option == sport_list[1]: # běh
            values = Run.plan_getRunDetails(master)
        return values