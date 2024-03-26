#importy knihovan
import customtkinter as ctk
from tkinter import *
#importy souborů
from sports.sport import Sport
from configuration import sport_list, sport_color, unknown_text, pie_chart_palette
from ctkWidgets import Label, Entry, CheckBox
from general import General

class Swim (Sport):
    """Třída pro funkce, které jsou specifické pro trénink typu posilovna."""
    def __init__(self):
        super().__init__()
        self.name = sport_list[0]
        self.color = sport_color[self.name]

    def createAttributes(self, training : object) -> list:
        self.message_attributes = ["datum", "sport", "čas", "cviky"]
        return self.message_attributes

    def createValues(self, training : object) -> list:
        """Metoda vytvoří list  atributů pro vepsání do tooltip message."""
        str_time  = str(training.time) + " min"
        self.message_values = [training.date, training.sport, str_time, training.practicedParts]
        return self.message_values

    @staticmethod
    def sortSwimTrainingList (master : object, training_list : list) -> list:
        """Roztřídí skupinu tréninků posilovna."""
        # TODO - třídění
        return training_list
    
    @staticmethod
    def plan_initSwimDetails (master : object) -> None:
        """Vytvoří widgety v framíku v detailech nastavování sportu (posilovna) ve vytváření
        cyklického tréninkového plánu."""
        # očekávaný čas
        time_l = Label(master, "Očekávaný čas:", ("Arial", 11))
        time_l.pack(side=TOP)
        time_l.configure(anchor = "w", width = 95)
        master.estimated_time = StringVar()
        time_e = Entry(master, master.estimated_time)
        time_e.pack(side=TOP)
        time_e.configure(width = 95)
        # upavaná vzdálenost
        dist_l = Label(master, "Očekávaná\ndistance:", ("Arial", 11))
        dist_l.pack(side=TOP, pady = 5)
        dist_l.configure(anchor = "w", width = 95)
        master.estimated_dist = StringVar()
        dist_e = Entry(master, master.estimated_dist)
        dist_e.pack(side=TOP)
        dist_e.configure(width = 95)

    @staticmethod
    def plan_getSwimDetails (master : object) -> tuple:
        """Vrátí data vložené do framíku sportu (plavání) v nastavování cyklického tréninkového plánu 
        -> nastavení detailů sportu"""
        time = Sport.floatEntryChecker(master.estimated_time.get())
        dist = Sport.floatEntryChecker(master.estimated_dist.get())
        return (time, dist)

    @staticmethod
    def swimData(master : object, data_list : list, index_adjustment = 2) -> None:
        """Rozklíčuje data z získané z tréninkové databáze pokud se
        jedná o trénink posilovna.
        Index_adjustment je úprava indexu, pokud tam chci poslat pole kde ty atributy neberu od 0."""
        master.time = General.checkKnownFloat(data_list[0 + index_adjustment])
        master.distance = General.checkKnownFloat(data_list[1 + index_adjustment])

    @staticmethod
    def plan_getSwimData (master : object, data : tuple) -> None:
        """Přiřadí zadané data tréninku typu posilovna."""
        master.distance = data[1]
    
    @staticmethod
    def plan_swimDataToList(training : object) -> list:
        """Zapíše vlastnosti tréninku plavání do listu informací o tréninku."""
        data_list = [training.date, training.sport, training.time, training.distance]
        return data_list

    @staticmethod
    def swimDetailsInOverview (master : object):
        """Metoda pro vytvoření specifických údajů o tréninku plavání do tabulky přehledu tréninků."""
        distance_text = str(master.training.distance) + " km"
        distance_l = Label(master, distance_text)
        distance_l.pack(side = LEFT, fill = ctk.Y)
        distance_l.configure(width = 250, height = 40, anchor = ctk.W)
        master.content_wigets.append(distance_l)

    @staticmethod
    def setFrameSwimWidgets (master : object):
        """Vytvoření nastavovacích okének pro přidání tréninku PLAVÁNÍ."""
        # zadání kilometrů
        Label(master, 'Kilometry (km)').pack(anchor=ctk.W)
        Entry(master, master.var_distance).pack(anchor=ctk.W)
        master.distance_error_l = Label(master, "", ("Arial", 10))
        master.distance_error_l.pack(anchor=ctk.W, side=TOP)

    @staticmethod
    def swimListForFile(master : object, training_list : list) -> None:
        """Přidá k listu dat specifické informace o tréninku typu plavání pro zapsání dat do 
        tréninkové databáze."""
        training_list.extend([master.var_time.get(), master.var_distance.get()])
        return training_list
    
    @staticmethod
    def verifySwim (master : object) -> bool:
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
    
    @staticmethod
    def swimDistanceFiltrator(master : object, distance_swim_filter :list) -> list:
        """Vyfiltruje plavání podle uplavané vzdálenosti."""
        # pokud není filtr nastavený -> trénink projde filtrem vždy
        bottom_condition = False # podmínka při nezadaném spodním filtru
        top_condition = False # podmínika při nezadaném horním filtru
        # spodní hranice filtru
        if distance_swim_filter[0] == "":
            bottom_condition = True
            distance_swim_filter[0] = "0"
        # horní hranice filtru
        if distance_swim_filter[1] == "":
            top_condition = True
            distance_swim_filter[1] = "0"
        # vytřídění dat podle zadaných mezí
        filtered = []
        for training in master.filtered_data:
                if training.sport == sport_list[1]:
                    try:
                        float(training.distance)
                        if (((float(training.distance) >= float(distance_swim_filter[0])) or bottom_condition)
                            and ((float(training.distance) <= float(distance_swim_filter[1])) or top_condition)):
                            filtered.append(training)
                    except:
                        continue
                else:
                    filtered.append(training)
        return filtered

    def updateSwimGUI (master : object, training : object) -> None:
        """Vytvoří widgety v okně pro úpravu tréninků v Overview, pokud se vybere trénink plavání."""
        dist_l = Label(master, "Vzdálenost: ") # label
        dist_l.grid(column = 0, row = master.next_row, sticky = ctk.E)
        dist_l.configure()

        master.var_dist = StringVar()
        dist_e = Entry(master, master.var_dist) # entry
        dist_e.grid(column = 1, row = master.next_row, padx=master.label_padx)
        dist_e.configure(width = master.box_width)
        master.var_dist.set(Sport.hasAttribute(training, "distance", ""))

        master.specific_widgets = [dist_l, dist_e]
        master.next_row = master.next_row + 1

    def updateSwimData (master : object) -> None:
        """Přidá do listu self.main_values hodnoty specifické pro trénink plavání."""
        master.main_values.extend([master.var_dist.get()])

    def getSwimTrainings (master : object) -> list:
        """Vrátí list tréninků typu posilovna."""
        swim_trainings = []
        for training in master.trainings:
            if training.sport == sport_list[1]:
                swim_trainings.append(training)
        return swim_trainings
    
    def makeSwimContent (periods : list) -> list:
        """Vytvoří náplň pro koláčový graf podrobností uběhnutých kilometrů běhu."""
        distances = [0] * len(periods)
        i = 0
        for period in periods:
            for training in period:
                try:
                    distances[i] = distances[i] + training.distance
                except:
                    continue
            i = i + 1
        return distances
    
    def singlePlanSwim (master : object) -> None:
        """Vytvoří widgety pro nastavení tréninku plavání v nastavení jednoduchého tréninkového plánu."""
        distance_label = Label(master, "Očekávaná\nvzdálenost:")
        distance_label.grid(row = 0, column = 0, sticky = "E", pady = 2)
        master.var_distance = StringVar()
        master.distance_entry = Entry(master, master.var_distance)
        master.distance_entry.grid(row = 0, column = 1, sticky = "W", padx = 5, pady = 2)
        master.distance_entry.configure(width = master.entry_width)

    @staticmethod
    def singlePlanEntry (master : object) -> bool:
        """Ověření uživatelského vstupu do detailního framu v singlePlan. Pokud je vstup správný, nastaví získaná data do vlastnosti rodičovského objektu frame_data."""
        float_entry = General.checkFloatEntry(master.var_distance.get())
        unknown_entry = master.var_distance.get() == ""
        if float_entry or unknown_entry:
            General.setDefaultBorder(master.distance_entry)
            master.frame_data = [master.var_distance.get()]
            return True
        General.setRedBorder(master.distance_entry)
        return False