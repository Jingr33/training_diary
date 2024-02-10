#import knihoven
import customtkinter as ctk
from tkinter import *
#importy souborů
from sports.sport import Sport
from configuration import sport_list, sport_color
from ctkWidgets import Label, Entry

class Run (Sport):
    """Třída pro funkce, které jsou specifické pro trénink typu běh."""
    def __init__(self):
        super().__init__()
        self.name = sport_list[1]
        self.color = sport_color[self.name]

    def createAttributes(self, training : object) -> list:
        """List názvů atributů tréninku vypisujících se do tooltipů."""
        self.message_attributes = ["datum", "sport", "čas", "vzdálenost"]
        return self.message_attributes

    def createValues(self, training : object) -> list:
        """Metoda vytvoří list  atributů pro vepsání do tooltip message."""
        str_time = str(training.time) + " min"
        str_distance = str(training.distance) + " km"
        self.message_values = [training.date, training.sport, str_time, str_distance]
        return self.message_values

    @staticmethod
    def sortRunTrainingList (master : object, trainings : list) -> list:
        """Roztřídí skupinu tréninků běh."""
        # list indexů pro slovníky
        index_list = master._indexList(len(trainings))
        # slovník tréninků
        trainings_dict = master._trainingDict(trainings, index_list)
        # slovník časů pro třídění
        sort_elems = master._sortDistanceDict(trainings, index_list)
        # roztříděný list tréninků
        to_sort = master._sortIt(sort_elems, trainings_dict)
        return to_sort
    
    @staticmethod
    def plan_initRunDetails(master : object) -> None:
        """Vytvoří widgety v framíku v detailech nastavování sportu (běh) ve vytváření
        cyklického tréninkového plánu."""
        # widgety očekávaného času
        time_l = Label(master, "Očekávaný čas:", ("Arial", 11))
        time_l.pack(side=TOP)
        time_l.configure(anchor = "w", width = 95)

        master.estimated_time = StringVar()
        time_e = Entry(master, master.estimated_time)
        time_e.pack(side=TOP)
        time_e.configure(width = 95)

        # widgety očekávané uběhnuté vzálenosti
        dist_l = Label(master, "Očekávaná\ndistance:", ("Arial", 11))
        dist_l.pack(side=TOP, pady = 5)
        dist_l.configure(anchor = "w", width = 95)

        master.estimated_dist = StringVar()
        dist_e = Entry(master, master.estimated_dist)
        dist_e.pack(side=TOP)
        dist_e.configure(width = 95)

    @staticmethod
    def plan_getRunDetails (master : object) -> tuple:
        """Ověří platnost dat a vrátí data vložené do framíku sportu (běh) v nastavování cyklického tréninkového plánu 
        -> nastavení detailů sportu"""
        time = Sport.floatEntryChecker(master.estimated_time.get())
        dist = Sport.floatEntryChecker(master.estimated_dist.get())
        return (time, dist)
    
    @staticmethod
    def runData(master : object,  data_list : list) -> None:
        """Rozklíčuje data z tréninkové databáze pokud se jedná 
        o běžeckéhý trénink."""
        master.time = data_list[2]
        master.distance = data_list[3]

    @staticmethod
    def plan_getRunData (master : object, data : tuple) -> None:
        """Přiřadí zadané data tréninku typu běh."""
        master.distance = data[1]

    @staticmethod
    def plan_runDataToList(training : object) -> list:
        """Zapíše vlastnosti tréninku posilovna do listu."""
        data_list = [training.date, training.time, training.distance]
        return data_list

    @staticmethod
    def setFrameRunWidgets (master : object):
        """Vytvoření nastavovacích okének pro přidání tréninku BĚH."""
        # zadání kilometrů
        Label(master, 'Kilometry (km)').pack(anchor=ctk.W)
        Entry(master, master.var_distance).pack(anchor=ctk.W)
        master.distance_error_l = Label(master, "", ("Arial", 10))
        master.distance_error_l.pack(anchor=ctk.W, side=TOP)

    @staticmethod
    def RunListForFile(master : object, training_list : list) -> None:
        """Přidá k listu dat specifické informace o tréninku typu běh pro zapsání dat do 
        tréninkové databáze."""
        training_list.extend([master.var_time.get(), master.var_distance.get()])
        return training_list
      
    def verifyRun (master : object) -> bool:
        """Ověří vstupy posilovny při zadávání nového tréninku."""
        entry = master.var_distance.get()
        verify_distance = False
        try:
            if entry:
                float(entry)
                master.distance_error_l.configure(text = "")
            verify_distance = True
        except:
            master.distance_error_l.configure(text_color = 'red', text="Špatně zadaná hodnota.")
        return verify_distance


