#importy knihovan
import customtkinter as ctk
from tkinter import *
from icecream import ic
#importy souborů
from sports.sport import Sport
from configuration import swim_style, unknown_text_label
import globalVariables as GV
from ctkWidgets import Label, Entry, CheckBox
from general import General

class Swim (Sport):
    """Třída pro funkce, které jsou specifické pro trénink typu posilovna."""
    def __init__(self):
        super().__init__()
        self.name = GV.sport_list[0]
        self.color = GV.sport_color[self.name]

    def createAttributes(self, training : object) -> list:
        """List názvů atributů tréninku vypisujících se do tooltipů."""
        self.message_attributes = ["datum", "sport", "čas", "vzdálenost", "styl"]
        return self.message_attributes

    def createValues(self, training : object) -> list:
        """Metoda vytvoří list  atributů pro vepsání do tooltip message."""
        str_time  = "{0} min".format(training.time)
        str_distance = "{0} km".format(training.distance)
        training.style_str = Swim.getSwimStyle(training)
        self.message_values = [training.date, training.sport, str_time, str_distance, training.style_str]
        return self.message_values
    
    @staticmethod
    def getSwimStyle (master : object) -> str:
        """Vytvoří string plaveckých stylů v daném tréninku (pro zobrazení např. v tooltipu)."""
        string = ""
        for i in range(len(swim_style)):
            if int(master.style[i]) == 1:
                string = "{0}{1}, ".format(string, swim_style[i])
        string = string[:-2]
        if not string: # pokud je string prázdný
            string = unknown_text_label
        return string

    @staticmethod
    def sortSwimTrainingList (master : object, trainings : list) -> list:
        """Roztřídí skupinu tréninků posilovna."""
        # vyřazení tréninků, které nejdou setřídit
        trainings = master.elimUnsortable(trainings, "distance")
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
    def plan_initSwimDetails (master : object) -> None:
        """Vytvoří widgety v framíku v detailech nastavování sportu (posilovna) ve vytváření
        cyklického tréninkového plánu."""
        font = ("Arial", 11)
        # očekávaný čas
        time_l = Label(master, "Očekávaný čas:", font)
        time_l.pack(side=TOP)
        time_l.configure(anchor = "w", width = 95)
        master.estimated_time = StringVar()
        time_e = Entry(master, master.estimated_time)
        time_e.pack(side=TOP)
        time_e.configure(width = 95)
        # upavaná vzdálenost
        dist_l = Label(master, "Očekávaná\ndistance:", font)
        dist_l.pack(side=TOP, pady = 5)
        dist_l.configure(anchor = "w", width = 95)
        master.estimated_dist = StringVar()
        dist_e = Entry(master, master.estimated_dist)
        dist_e.pack(side=TOP)
        dist_e.configure(width = 95)
        # plvacký styl
        style_l = Label(master, "Plavecký styl: ", font)
        style_l.pack(side = TOP, pady = 5, anchor = "w")
        style_l.configure(width = 95)
        master.estimated_style = [0] * len(swim_style)
        for i in range(len(swim_style)):
            chb_var = IntVar()
            checkbox = CheckBox(master, swim_style[i], chb_var)
            checkbox.pack(side = TOP)
            master.estimated_style[i] = chb_var

    @staticmethod
    def plan_getSwimDetails (master : object) -> tuple:
        """Vrátí data vložené do framíku sportu (plavání) v nastavování cyklického tréninkového plánu 
        -> nastavení detailů sportu"""
        time = Sport.floatEntryChecker(master.estimated_time.get())
        dist = Sport.floatEntryChecker(master.estimated_dist.get())
        style = [intvar.get() for intvar in master.estimated_style]
        return (time, dist, style)

    @staticmethod
    def swimData(master : object, data_list : list, index_adjustment = 2) -> None:
        """Rozklíčuje data z získané z tréninkové databáze pokud se
        jedná o trénink plavání.
        Index_adjustment je úprava indexu, pokud tam chci poslat pole kde ty atributy neberu od 0."""
        master.time = General.checkKnownFloat(data_list[0 + index_adjustment])
        master.distance = General.checkKnownFloat(data_list[1 + index_adjustment])
        master.style = [data_list[i + 2 + index_adjustment] for i in range(len(swim_style))]
        master.style_str = Swim.getSwimStyle(master)

    @staticmethod
    def plan_getSwimData (master : object, data : tuple) -> None:
        """Přiřadí zadané data tréninku typu plavání."""
        master.distance = data[1]
        master.style = data[2]
    
    @staticmethod
    def plan_swimDataToList(training : object) -> list:
        """Zapíše vlastnosti tréninku plavání do listu informací o tréninku."""
        data_list = [training.date, training.sport, training.time, training.distance] + training.style
        return data_list

    @staticmethod
    def swimDetailsInOverview (master : object):
        """Metoda pro vytvoření specifických údajů o tréninku plavání do tabulky přehledu tréninků."""
        details_text = "{0} km - Styl: {1}".format(General.setUnknownText(master.training.distance), General.setUnknownText(master.training.style_str))
        details_l = Label(master, details_text)
        details_l.pack(side = LEFT, fill = ctk.Y)
        details_l.configure(width = 250, height = 40, anchor = ctk.W)
        master.content_wigets.append(details_l)

    @staticmethod
    def setFrameSwimWidgets (master : object):
        """Vytvoření nastavovacích okének pro přidání tréninku PLAVÁNÍ."""
        # zadání kilometrů
        Label(master, 'Kilometry (km)').pack(anchor=ctk.W)
        Entry(master, master.var_distance).pack(anchor=ctk.W)
        master.distance_error_l = Label(master, "", ("Arial", 10))
        master.distance_error_l.pack(anchor=ctk.W, side=TOP)
        # zadání plaveckého stylu
        Label(master, 'Plavecký styl').pack(anchor = ctk.W)
        master.checkboxes = [None] * len(swim_style)
        for i in range(len(swim_style)):
            var = IntVar()
            chb = CheckBox(master, swim_style[i], var)
            chb.pack(anchor = ctk.W, padx = 10)
            master.checkboxes[i] = var

    @staticmethod
    def swimListForFile(master : object, training_list : list) -> None:
        """Přidá k listu dat specifické informace o tréninku typu plavání pro zapsání dat do 
        tréninkové databáze."""
        style_list = [intvar.get() for intvar in master.checkboxes]
        training_list.extend([master.var_time.get(), master.var_distance.get()])
        training_list.extend(style_list)
        return training_list
    
    @staticmethod
    def verifySwim (master : object) -> bool:
        """Ověří vstupy plavání při zadávání nového tréninku."""
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
    def swimDistanceFiltrator(master : object, distance_swim_filter : list) -> list:
        """Vyfiltruje plavání podle uplavané vzdálenosti."""
        # pokud není filtr nastavený -> trénink projde filtrem vždy
        bottom_condition = False # podmínka při nezadaném spodním filtru
        top_condition = False # podmínika při nezadaném horním filtru
        min_distance = distance_swim_filter[0].strip()
        max_distance = distance_swim_filter[1].strip()
        # spodní hranice filtru
        if min_distance == "":
            bottom_condition = True
            min_distance = "0"
        # horní hranice filtru
        if max_distance == "":
            top_condition = True
            max_distance = "0"
        # vytřídění dat podle zadaných mezí
        filtered = []
        for training in master.filtered_data:
                if training.sport == GV.sport_list[2]:
                    try:
                        train_distance = float(training.distance)
                        if (((train_distance >= float(min_distance)) or bottom_condition)
                            and ((train_distance <= float(max_distance)) or top_condition)):
                            filtered.append(training)
                    except:
                        continue
                else:
                    filtered.append(training)
        return filtered
    
    @staticmethod
    def swimStyleFiltrator (master : object, trainings_for_filter : list) -> list:
        """Vyfiltruje plavání podle zvolených stylů a vyfiltrovaný list tréninků."""
        ...
        return master.filtered_data

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
        """Vrátí list tréninků typu plavání."""
        swim_trainings = []
        for training in master.trainings:
            if training.sport == GV.sport_list[1]:
                swim_trainings.append(training)
        return swim_trainings
    
    def makeSwimContent (periods : list) -> list:
        """Vytvoří náplň pro koláčový graf podrobností uplavaných kilometrů běhu."""
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
        # plavecký styl
        style_label = Label(master, "Plavecký \nstyl: ")
        style_label.grid(row = 1, column = 0, sticky = "E", pady = 2)
        master.checkboxes = [None] * len(swim_style)
        for i in range(len(swim_style)):
            var = IntVar()
            chb = CheckBox(master, swim_style[i], var)
            chb.grid(row = (1+i), column = 1, sticky = "W", padx = 5, pady = 2)
            master.checkboxes[i] = var

    @staticmethod
    def singlePlanEntry (master : object) -> bool:
        """Ověření uživatelského vstupu do detailního framu v singlePlan. Pokud je vstup správný, nastaví získaná data do vlastnosti rodičovského objektu frame_data."""
        float_entry = General.checkFloatEntry(master.var_distance.get())
        unknown_entry = master.var_distance.get() == ""
        if float_entry or unknown_entry:
            General.setDefaultBorder(master.distance_entry)
            master.frame_data = [master.var_distance.get()]
            master.frame_data.extend(intvar.get() for intvar in master.checkboxes)
            return True
        General.setRedBorder(master.distance_entry)
        return False