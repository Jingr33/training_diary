# importy souborů
from sports.sport import Sport
from sports.gym import Gym
from sports.run import Run
from configuration import sport_list, free_day

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
    def plan_setSportDetails(master : object, option : str) -> None:
        """Rozhodne, které podrobnosti sportu ve tvoření cyklického tréninkového plánu
        se vytvoří a zavolá danou funkci z objektu daného sportu."""
        if option == sport_list[0]: # posilovna
            Gym.plan_initGymDetails(master)
        elif option == sport_list[1]: # běh
            Run.plan_initRunDetails(master)

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
        
    @staticmethod
    def plan_getSportDetails(master : object, option : str) -> tuple:
        """Rozhodne, ze kterého sportu data pochází a získá je."""
        if option == sport_list[0]: # posilovna
            values = Gym.plan_getGymDetails(master)
        elif option == sport_list[1]: # běh
            values = Run.plan_getRunDetails(master)
        return values
    
    @staticmethod
    def whichSport (sport_name : str) -> str:
        """Zjistí, o který sport se jedná. Metoda hlavně pro objekt one trainig"""
        sport = ""
        if sport_name == sport_list[0]:
            sport = sport_list[0]
        elif sport_name == sport_list[1]:
            sport = sport_list[1]
        else:
            ... #TODO
        return sport
    
    @staticmethod
    def findData(master : object, data_list : list) -> None:
        """Rozhodne o který sport se jedná a rozklíčuje jeho 
        data získané z databáze tréninků."""
        if master.sport == sport_list[0]:
            Gym.gymData(master, data_list)
        elif master.sport == sport_list[1]:
            Run.runData(master, data_list)
        else:
            ... #TODO

    @staticmethod
    def plan_getSportData (master : object, data: tuple) -> None:
        """Vytáhne data ze získaného tuplu a pro každý sport přiřadí vlastnosti tréninku."""
        if master.sport == sport_list[0]: #posilovna
            Gym.plan_getGymData(master, data)
        elif master.sport == sport_list[1]: # běh
            Run.plan_getRunData(master, data)
        else:
            ... #TODO

    @staticmethod
    def plan_trainingToList(training : object) -> list:
        """Převede data tréninku na list údajů zapsatelných do souboru."""
        if training.sport == sport_list[0]: # posilovna
            data_list = Gym.plan_gymDataToList(training)
        elif training.sport == sport_list[1]: # běh
            data_list = Run.plan_runDataToList(training)
        # další sporty ...
        elif training.sport == free_day: # volný den
            data_list = Sport.plan_FreeDayDataToList(training)
        return data_list
    
    @staticmethod
    def detailsInOverview (master : object) -> None:
        """Vytvoří label pro obsah detalního popisu tréninku v OneRow v přehledu tréninků."""
        if master.training.sport == sport_list[0]: # posilovna
            Gym.gymDetailsInOverview(master)
        elif master.training.sport == sport_list[1]: # běh
            Run.runDetailsInOverview(master)

