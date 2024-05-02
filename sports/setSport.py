# importy souborů
from sports.gym import Gym
from sports.run import Run
from sports.swim import Swim
from general import General
from configuration import gym_chart_strings, run_chart_strings, unknown_text, all_sports
import globalVariables as GV
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
        sport_funcs = [Gym.plan_initGymDetails, Run.plan_initRunDetails, Swim.plan_initSwimDetails]
        for i in range(len(all_sports)):
            if option == all_sports[i]:
                sport_funcs[i](master)

    @staticmethod
    def sortEachTrainingDict (master : object, training_dict : dict, key : str) -> list:
        """Vezme vložený slovník a rozhodne, zda a jakým způsobem se tento list třídí, 
        vrátí setříděný list tréninků.
        Vstup: 1) slovník s listy rozdělených tréninků,)
               2) klíč sportu, který se má setřídít."""
        # rozhodne o který sport se jedná
        sport_funcs = [Gym.sortGymTrainingList, Run.sortRunTrainingList, Swim.sortSwimTrainingList]
        for i in range(len(all_sports)):
            if key == all_sports[i]:
                return sport_funcs[i](master, training_dict[key])
        
    @staticmethod
    def plan_getSportDetails(master : object, option : str) -> tuple:
        """Rozhodne, ze kterého sportu data pochází a získá je."""
        sport_funcs = [Gym.plan_getGymDetails, Run.plan_getRunDetails, Swim.plan_getSwimDetails]
        for i in range(len(all_sports)):
            if option == all_sports[i]:
                return sport_funcs[i](master)
    
    @staticmethod
    def whichSport (sport_name : str) -> str:
        """Zjistí, o který sport se jedná. Metoda hlavně pro objekt OneTrainig."""
        for i in range(len(all_sports)):
            if sport_name == all_sports[i]:
                return all_sports[i]
    
    @staticmethod
    def findData(master : object, data_list : list, index_adjustment = 2) -> None:
        """Rozhodne o který sport se jedná a rozklíčuje jeho 
        data získané z databáze tréninků.
        Index_adjustment je úprava indexu pro data, pokud tam chci poslat pole kde ty atributy neberu od 0."""
        sport_funcs = [Gym.gymData, Run.runData, Swim.swimData]
        for i in range(len(all_sports)):
            if master.sport == all_sports[i]:
                sport_funcs[i](master, data_list, index_adjustment)

    @staticmethod
    def plan_getSportData (master : object, data: tuple) -> None:
        """Vytáhne data ze získaného tuplu a pro každý sport přiřadí vlastnosti tréninku."""
        sport_funcs = [Gym.plan_getGymData, Run.plan_getRunData, Swim.plan_getSwimData]
        for i in range(len(all_sports)):
            if master.sport == all_sports[i]:
                sport_funcs[i](master, data)

    @staticmethod
    def plan_trainingToList(training : object) -> list:
        """Převede data tréninku na list údajů zapsatelných do souboru."""
        sport_funcs = [Gym.plan_gymDataToList, Run.plan_runDataToList, Swim.plan_swimDataToList]
        for i in range(len(all_sports)):
            if training.sport == all_sports[i]:
                return sport_funcs[i](training)
    
    @staticmethod
    def detailsInOverview (master : object) -> None:
        """Vytvoří label pro obsah detalního popisu tréninku v OneRow v přehledu tréninků."""
        sport_funcs = [Gym.gymDetailsInOverview, Run.runDetailsInOverview, Swim.swimDetailsInOverview]
        for i in range(len(all_sports)):
            if master.training.sport == all_sports[i]:
                sport_funcs[i](master)

    @staticmethod
    def setFrameWidgets (master : object, choice : str) -> None:
        """Rozhodne, o který sport se jedná a vytvoří widgety pro nastavení tréninku daného sportu."""
        sport_funcs = [Gym.setFrameGymWidgets, Run.setFrameRunWidgets, Swim.setFrameSwimWidgets]
        for i in range(len(all_sports)):
            if choice == all_sports[i]:
                sport_funcs[i](master)

    @staticmethod
    def fillListForFile (master : object, training_list : list) -> list:
        """Rozhodne, o který sport se jedná a přidá k listu dat o tréninku specifické informace 
        o sportu, který obsahuje do tréninkové databáze. Vrátí list s tréninkovými daty."""
        sport_funcs = [Gym.gymListForFile, Run.runListForFile, Swim.swimListForFile]
        for i in range(len(all_sports)):
            if training_list[1] == all_sports[i]:
                return sport_funcs[i](master, training_list)
    
    @staticmethod
    def verifyDetails (master : object) -> bool:
        """Ověří vsupy detailů sportu při zadávání tréninku."""
        sport_funcs = [Gym.verifyGym, Run.verifyRun, Swim.verifySwim]
        for i in range(len(all_sports)):
            if master.choice == all_sports[i]:
                return sport_funcs[i](master)

    @staticmethod
    def detailsFiltrator (master : object, detail_filter : list) -> list:
        """Vyfiltruje data podle detalních možností jednotlivých sportů."""
        # detaily posilovny
        if sum(detail_filter[0]):
            master.filtered_data = Gym.gymPartsFiltrator(master, detail_filter[0])
        # detaily běhu
        master.filtered_data = Run.runDistanceFiltrator(master, detail_filter[1])
        # vyfiltrování detailů plavání
        master.filtered_data = Swim.swimDistanceFiltrator(master, detail_filter[2])
        master.filtered_data = Swim.swimStyleFiltrator(master, detail_filter[2])

    @staticmethod
    def updateTrainingGUI (master : object, training : object, value : str) -> None:
        """Vytvoří specifické GUI pro daný trénink, při updatování tréninkových hodnot."""
        sport_funcs = [Gym.updateGymGUI, Run.updateRunGUI, Swim.updateSwimGUI]
        for i in range(len(all_sports)):
            if value == all_sports[i]:
                sport_funcs[i](master, training)

    @staticmethod
    def updateTrainingData (master : object) -> None:
        """Získá data zadaná uživatelem v okně pro úpravu jednotlivého tréninku v Overview tréninků."""
        sport_funcs = [Gym.updateGymData, Run.updateRunData, Swim.updateSwimData]
        for i in range(len(all_sports)):
            if master.main_values == all_sports[i]:
                sport_funcs[i](master)

    @staticmethod
    def getOneSportTrainings(master : object, sport : str) -> list:
        """Vrátí list tréninků patřící zadanému sportu."""
        sport_funcs = [Gym.getGymTrainings, Run.getRunTrainings, Swim.getSwimTrainings]
        for i in range(len(all_sports)):
            if sport == all_sports[i]:
                return sport_funcs[i](master)
    
    @staticmethod
    def makeChartContent (trainings : list, sport : str) -> list:
        """Vrátí list podrobností o trénincích jednotlivých sportů."""
        sport_funcs = [Gym.makeGymContent, Run.makeRunContent, Swim.makeSwimContent]
        for i in range(len(all_sports)):
            if sport == all_sports[i]:
                return sport_funcs[i](trainings)
    
    @staticmethod
    def chooseChartType (sport : str):
        """Metoda vrátí typ grafu, který se má použít a slovník stringů pro naplnění popisků grafu."""
        if sport == all_sports[0]: # posilovna
            chart_type = "pie"
            chart_strings = gym_chart_strings
        elif sport == all_sports[1] or all_sports[2]: # běh
            chart_type = "bar"
            chart_strings = run_chart_strings
        return chart_type, chart_strings
    
    @staticmethod
    def singlePlanDetails (master : object, sport : str) -> None:
        """Metoda vytvoří obsah framu s nastavením podrobností tréninku podle sportu v jednoduchém nastavení tréninkového plánu."""
        sport_funcs = [Gym.singlePlanGym, Run.singlePlanRun, Swim.singlePlanSwim]
        for i in range(len(all_sports)):
            if sport == all_sports[i]:
                sport_funcs[i](master)

    @staticmethod
    def singlePlanEntry (master : object, sport : str) -> list:
        """Ověření uživatelského vstupu do detailního framu v singlePlan. Zároveň nastaví do vlastnosti frame_data rodičovského objektu zadaná data (pokud jsou správné)."""
        sport_funcs = [Gym.singlePlanEntry, Run.singlePlanEntry, Swim.singlePlanEntry]
        for i in range(len(all_sports)):
            if sport == all_sports[i]:
                return sport_funcs[i](master)