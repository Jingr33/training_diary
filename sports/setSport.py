# importy souborů
from sports.sport import Sport
from sports.gym import Gym
from sports.run import Run
from sports.swim import Swim
from general import General
from configuration import sport_list, free_day, gym_chart_strings, run_chart_strings, unknown_text
from icecream import ic

class SetSport():
    """Třída pro nastavení základních vlastností pro jednotlivé sporty."""
    
    def createTooltipMessage(self, training : object) -> str:
        """Metoda určí, o který sport se jedná a pomocí dalších objektů vytvoří tooltip message."""
        sport_objects = {"posilovna" : Gym, 
                         "běh" : Run, 
                         "plavání" : Swim}
        message = self._oneSportMessage(sport_objects, training)
        message = General.setStringForUndefined(message, ["None", unknown_text])
        return message
    
    def _oneSportMessage (self, sport_object : dict, training : object) -> str:
        """Vytvoří zprávu pro tooltip sportu v kalendáři podle zadaného typu tréninku."""
        sport = sport_object[training.sport]()
        sport.createAttributes(training)
        sport.createValues(training)
        message = sport.tooltipMessage()
        return message
    
    @staticmethod
    def plan_setSportDetails(master : object, option : str) -> None:
        """Rozhodne, které podrobnosti sportu ve tvoření cyklického tréninkového plánu
        se vytvoří a zavolá danou funkci z objektu daného sportu."""
        if option == sport_list[0]: # posilovna
            Gym.plan_initGymDetails(master)
        elif option == sport_list[1]: # běh
            Run.plan_initRunDetails(master)
        elif option == sport_list[2]: # plavání
            Swim.plan_initSwimDetails(master)

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
        elif key == sport_list[2]:
            training_dict[key] = Swim.sortSwimTrainingList(master, training_dict[key])
        return training_dict[key]
        
    @staticmethod
    def plan_getSportDetails(master : object, option : str) -> tuple:
        """Rozhodne, ze kterého sportu data pochází a získá je."""
        if option == sport_list[0]: # posilovna
            values = Gym.plan_getGymDetails(master)
        elif option == sport_list[1]: # běh
            values = Run.plan_getRunDetails(master)
        elif option == sport_list[2]:
            values = Swim.plan_getSwimDetails(master)
        return values
    
    @staticmethod
    def whichSport (sport_name : str) -> str:
        """Zjistí, o který sport se jedná. Metoda hlavně pro objekt onetrainig"""
        sport = ""
        if sport_name == sport_list[0]:
            sport = sport_list[0]
        elif sport_name == sport_list[1]:
            sport = sport_list[1]
        elif sport_name == sport_list[2]:
            sport = sport_list[2]
        return sport
    
    @staticmethod
    def findData(master : object, data_list : list, index_adjustment = 2) -> None:
        """Rozhodne o který sport se jedná a rozklíčuje jeho 
        data získané z databáze tréninků.
        Index_adjustment je úprava indexu pro data, pokud tam chci poslat pole kde ty atributy neberu od 0."""
        if master.sport == sport_list[0]:
            Gym.gymData(master, data_list, index_adjustment)
        elif master.sport == sport_list[1]:
            Run.runData(master, data_list, index_adjustment)
        elif master.sport == sport_list[2]:
            Swim.swimData(master, data_list, index_adjustment)

    @staticmethod
    def plan_getSportData (master : object, data: tuple) -> None:
        """Vytáhne data ze získaného tuplu a pro každý sport přiřadí vlastnosti tréninku."""
        if master.sport == sport_list[0]: #posilovna
            Gym.plan_getGymData(master, data)
        elif master.sport == sport_list[1]: # běh
            Run.plan_getRunData(master, data)
        elif master.sport == sport_list[2]: # plavání
            Swim.plan_getSwimData(master, data)

    @staticmethod
    def plan_trainingToList(training : object) -> list:
        """Převede data tréninku na list údajů zapsatelných do souboru."""
        if training.sport == sport_list[0]: # posilovna
            data_list = Gym.plan_gymDataToList(training)
        elif training.sport == sport_list[1]: # běh
            data_list = Run.plan_runDataToList(training)
        elif training.sport == sport_list[2]: # plavání
            data_list = Swim.plan_swimDataToList(training)
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
        elif master.training.sport == sport_list[2]: # plavání
            Swim.swimDetailsInOverview(master)

    @staticmethod
    def setFrameWidgets (master : object, choice : str) -> None:
        """Rozhodne, o který sport se jedná a vytvoří widgety pro nastavení tréninku daného sportu."""
        if choice == sport_list[0]:
            Gym.setFrameGymWidgets(master)
        elif choice == sport_list[1]:
            Run.setFrameRunWidgets(master)
        elif choice == sport_list[2]:
            Swim.setFrameSwimWidgets(master)

    @staticmethod
    def fillListForFile (master : object, training_list : list) -> list:
        """Rozhodne, o který sport se jedná a přidá k listu dat o tréninku specifické informace 
        o sportu, který obsahuje do tréninkové databáze. Vrátí list s tréninkovými daty."""
        if training_list[1] == sport_list[0]:
            training_list = Gym.gymListForFile(master, training_list)
        elif training_list[1] == sport_list[1]:
            training_list = Run.runListForFile(master, training_list)
        elif training_list[1] == sport_list[2]:
            training_list = Swim.swimListForFile(master, training_list)
        return training_list
    
    @staticmethod
    def verifyDetails (master : object) -> bool:
        """Ověří vsupy detailů sportu při zadávání tréninku."""
        if master.choice == sport_list[0]: # posilovna
            verified = Gym.verifyGym(master)
        elif master.choice == sport_list[1]: #běh
            verified = Run.verifyRun(master)
        elif master.choice == sport_list[2]: # plavání
            verified = Swim.verifySwim(master)
        return verified
    
    @staticmethod
    def detailsFiltrator (master : object, detail_filter : list) -> list:
        """Vyfiltruje data podle detalních možností sportů."""
        # detaily posilovny
        if detail_filter[0]:
            master.filtered_data = Gym.gymPartsFiltrator(master, detail_filter[0])
        # detaily běhu
        master.filtered_data = Run.runDistanceFiltrator(master, detail_filter[1])
        # vyfiltrování detailů plavání
        master.filtered_data = Swim.swimDistanceFiltrator(master, detail_filter[2])
        master.filtered_data = Swim.swimStyleFiltrator(master, detail_filter[2])

    @staticmethod
    def updateTrainingGUI (master : object, training : object, value : str) -> None:
        """Vytvoří specifické GUI pro daný trénink, při udatování tréninkových hodnot."""
        if value == sport_list[0]: # posilovna
            Gym.updateGymGUI(master, training)
        elif value == sport_list[1]: # běh
            Run.updateRunGUI(master, training)
        elif value == sport_list[2]: # plavání
            Swim.updateSwimGUI(master, training)

    @staticmethod
    def updateTrainingData (master : object) -> None:
        """Získá data zadaná uživatelem v okně pro úpravu jednotlivého tréninku v Overview."""
        if master.main_values[1] == sport_list[0]: # posilovna
            Gym.updateGymData(master)
        elif master.main_values[1] == sport_list[1]: # běh
            Run.updateRunData(master)
        elif master.main_values[1] == sport_list[2]: # plavání
            Swim.updateSwimData(master)

    @staticmethod
    def getOneSportTrainings(master : object, sport : str) -> list:
        """Vrátí list tréninků patřící zadanému sportu."""
        if sport == sport_list[0]:  #posilovna
            trainings  = Gym.getGymTrainings(master)
        elif sport == sport_list[1]: # běh
            trainings = Run.getRunTrainings(master)
        elif sport == sport_list[1]: # plavání
            trainings = Swim.getSwimTrainings(master)
        return trainings
    
    @staticmethod
    def makeChartContent (trainings : list, sport : str) -> list:
        """Vrátí list podrobností o trénincích jednotlivých sportů."""
        if sport == sport_list[0]: # posilovna
            chart_content = Gym.makeGymContent(trainings)
        elif sport == sport_list[1]: # běh
            chart_content = Run.makeRunContent(trainings)
        elif sport == sport_list[2]: # plavání
            chart_content = Swim.makeSwimContent(trainings)
        return chart_content
    
    @staticmethod
    def chooseChartType (sport : str):
        """Metoda vrátí typ grafu, který se má použít a slovník stringů pro naplnění popisků grafu."""
        if sport == sport_list[0]: # posilovna
            chart_type = "pie"
            chart_strings = gym_chart_strings
        elif sport == sport_list[1] or sport_list[2]: # běh
            chart_type = "bar"
            chart_strings = run_chart_strings
        return chart_type, chart_strings
    
    @staticmethod
    def singlePlanDetails (master : object, sport : str) -> None:
        """Metoda vytvoří obsah framu s nastavením podrobností tréninku podle sportu v jednodichém nastavení tréninkového plánu."""
        if sport == sport_list[0]: # posilovna
            Gym.singlePlanGym(master)
        elif sport == sport_list[1]: #běh
            Run.singlePlanRun(master)
        elif sport == sport_list[2]: # plavání
            Swim.singlePlanSwim(master)

    @staticmethod
    def singlePlanEntry (master : object, sport : str) -> list:
        """Ověření uživatelského vstupu do detailního framu v singlePlan. Zároveň nastaví do vlastnosti frame_data rodičovského objektu zadaná data (pokud jsou správné)."""
        if sport == sport_list[0]: # posilovna
            return Gym.singlePlanEntry(master)
        elif sport == sport_list[1]: # běh
            return Run.singlePlanEntry(master)
        elif sport == sport_list[2]: # plavání
            return Swim.singlePlanEntry(master)
