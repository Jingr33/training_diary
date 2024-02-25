#importy knihovan
import customtkinter as ctk
from tkinter import *
#importy souborů
from sports.sport import Sport
from configuration import sport_list, sport_color, gym_body_parts, unknown_text, pie_chart_palette
from ctkWidgets import Label, Entry, CheckBox
from general import General

class Gym (Sport):
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
    def sortGymTrainingList (master : object, training_list : list) -> list:
        """Roztřídí skupinu tréninků posilovna."""
        # akorát, že posilovna se nijak netřídí...zatím
        return training_list
    
    @staticmethod
    def plan_initGymDetails (master : object) -> None:
        """Vytvoří widgety v framíku v detailech nastavování sportu (posilovna) ve vytváření
        cyklického tréninkového plánu."""
        # stringvar promenne pro ukládání zadaných dat
        master.estimated_time = StringVar()
        master.estim_leg = StringVar(value=0)
        master.estim_core = StringVar(value=0)
        master.estim_breast = StringVar(value=0)
        master.estim_shoulder = StringVar(value=0)
        master.estim_back = StringVar(value=0)
        master.estim_biceps = StringVar(value=0)
        master.estim_triceps = StringVar(value=0)
        master.estim_forearm = StringVar(value=0)

        # očekáváný strávený čas
        time_l = Label(master, "Očekávaný čas:")
        time_l.pack(side=TOP)
        time_l.configure(width = 95, anchor = 'w')

        time_e = Entry(master, master.estimated_time)
        time_e.pack(side=TOP)
        time_e.configure(width=95)

        # očekávané odvičené části těla
        parts_l = Label(master, "Cviky:")
        parts_l.pack(side=TOP)
        parts_l.configure(width=95, anchor='w')

        leg_chb = CheckBox(master, gym_body_parts[0], master.estim_leg)
        leg_chb.pack(side = TOP, pady=1)
        leg_chb.configure(width=95)

        core_chb = CheckBox(master, gym_body_parts[1], master.estim_core)
        core_chb.pack(side = TOP, pady=1)
        core_chb.configure(width=95)

        breast_chb = CheckBox(master, gym_body_parts[2], master.estim_breast)
        breast_chb.pack(side = TOP, pady=1)
        breast_chb.configure(width=95)

        shoulder_chb = CheckBox(master, gym_body_parts[3], master.estim_shoulder)
        shoulder_chb.pack(side = TOP, pady=1)
        shoulder_chb.configure(width=95)

        back_chb = CheckBox(master, gym_body_parts[4], master.estim_back)
        back_chb.pack(side = TOP, pady=1)
        back_chb.configure(width=95)

        biceps_chb = CheckBox(master, gym_body_parts[5], master.estim_biceps)
        biceps_chb.pack(side = TOP, pady=1)
        biceps_chb.configure(width=95)

        triceps_chb = CheckBox(master, gym_body_parts[6], master.estim_triceps)
        triceps_chb.pack(side = TOP, pady=1)
        triceps_chb.configure(width=95)

        forearm_chb = CheckBox(master, gym_body_parts[7], master.estim_forearm)
        forearm_chb.pack(side = TOP, pady=1)
        forearm_chb.configure(width=95)


    @staticmethod
    def plan_getGymDetails (master : object) -> tuple:
        """Vrátí data vložené do framíku sportu (běh) v nastavování cyklického tréninkového plánu 
        -> nastavení detailů sportu"""
        time = Sport.floatEntryChecker(master.estimated_time.get()) # kontrola vstupu času
        
        # list získaných hodnot z chceckboxů
        values_list = [master.estim_leg.get(), master.estim_core.get(), master.estim_breast.get(),
                master.estim_shoulder.get(), master.estim_back.get(), master.estim_biceps.get(),
                master.estim_triceps.get(), master.estim_forearm.get()]
        chceckbox_list = Sport.emptyCheckboxChecker(values_list) # kontrola zadání dat do chceckboxů
        return (time, chceckbox_list)

    @staticmethod
    def gymData(master : object, data_list : list, index_adjustment = 2) -> None:
        """Rozklíčuje data z získané z tréninkové databáze pokud se
        jedná o trénink posilovna.
        Index_adjustment je úprava indexu, pokud tam chci poslat pole kde ty atributy neberu od 0."""
        master.time = General.checkKnownInt(data_list[0 + index_adjustment])
        # zklouška, zda bylo něco zadáno
        if data_list[1 + index_adjustment] != unknown_text:
            master.leg = int(data_list[1 + index_adjustment])
            master.core = int(data_list[2 + index_adjustment])
            master.breast = int(data_list[3 + index_adjustment])
            master.shoulders = int(data_list[4 + index_adjustment])
            master.back = int(data_list[5 + index_adjustment])
            master.biceps = int(data_list[6 + index_adjustment])
            master.triceps = int(data_list[7 + index_adjustment])
            master.forearm = int(data_list[8 + index_adjustment])
            isset = (master.leg + master.core + master.breast + master.shoulders + master.back + 
                    master.biceps + master.triceps + master.forearm)

            # vytvoření vlastnosti practicedParts
            master.practicedParts = Gym.practicedPartsString(master)
        else:
            master.practicedParts = unknown_text

    @staticmethod
    def practicedPartsString (master : object):
        "Vytvoří string procvčených částí těla."
        # pole částí těla
        parts = [master.leg, master.core, master.breast, master.shoulders, master.back,
                 master.biceps, master.triceps, master.forearm]
        # vytvoření slovního podání odcvičených částí těla
        practiced_parts = ""
        text = ""
        i = 0
        for part in parts: # přes věechny možné odcvičené části těla
            if part == 1: # pokud byla odcvičena
                if practiced_parts != "": #udělá se mezery mezi slovy
                    text = ", "
                text = text + gym_body_parts[i]
                practiced_parts = practiced_parts + text
            i = i + 1
        return practiced_parts

    @staticmethod
    def plan_getGymData (master : object, data : tuple) -> None:
        """Přiřadí zadané data tréninku typu posilovna."""
        data_list = data[1]
        # vyhodnocení, zda je v listu něco zadáno
        data_check = Gym.tryGymData(data_list)
        # uložení dat
        if data_check:
            master.leg = int(data_list[0])
            master.core = int(data_list[1])
            master.breast = int(data_list[2])
            master.shoulders = int(data_list[3])
            master.back = int(data_list[4])
            master.biceps = int(data_list[5])
            master.triceps = int(data_list[6])
            master.forearm = int(data_list[7])
            # vytvoření vlastnosti practicedParts
            master.practicedParts = Gym.practicedPartsString(master)
        else:
            master.practicedParts = unknown_text

    @staticmethod
    def tryGymData (data_list : list) -> bool:
        """Vyhodnotí, zda je v listu jakákoliv zadaná hodnota -> True, jinak False."""
        try:
            int(data_list[2])
            check = True
        except:
            check = False
        return check
    
    @staticmethod
    def plan_gymDataToList(training : object) -> list:
        """Zapíše vlastnosti tréninku posilovna do listu."""
        # podmínka pro prázné data
        if training.practicedParts == unknown_text:
            data_list = [training.date, training.sport, training.time, unknown_text]
        else:
            # vytvoření listu
            data_list = [training.date, training.sport, training.time, training.leg, training.core, training.breast,
                        training.shoulders, training.back, training.biceps, training.triceps,
                        training.forearm]
        return data_list

    @staticmethod
    def gymDetailsInOverview (master : object):
        """Metoda pro vytvoření specifických údajů o posilovně do tabulky."""
        practiced_l = Label(master, master.training.practicedParts)
        practiced_l.pack(side = LEFT, fill = ctk.Y)
        practiced_l.configure(width = 250, height = 40, anchor = ctk.W)
        master.content_wigets.append(practiced_l)

    @staticmethod
    def setFrameGymWidgets (master : object):
        """Vytvoření nastavovacích okének pro přidání tréninku POSILOVNA."""
        # inicializace proměnných
        master.var_legs = StringVar(value=0)
        master.var_core = StringVar(value=0)
        master.var_breast = StringVar(value=0)
        master.var_shoulders = StringVar(value=0)
        master.var_back = StringVar(value=0)
        master.var_biceps = StringVar(value=0)
        master.var_triceps = StringVar(value=0)
        master.var_forearm = StringVar(value=0)
        # vytvoření checkboxů s odcvičenými částmi
        exercise_l = Label(master, "Odcvičeno")
        exercise_l.pack(anchor=ctk.W)
        leg_chb = CheckBox(master, gym_body_parts[0], master.var_legs)
        leg_chb.pack(anchor=ctk.W)
        core_chb = CheckBox(master, gym_body_parts[1], master.var_core)
        core_chb.pack(anchor=ctk.W)
        breast_chb = CheckBox(master, gym_body_parts[2], master.var_breast)
        breast_chb.pack(anchor=ctk.W)
        shoulders_chb = CheckBox(master, gym_body_parts[3], master.var_shoulders)
        shoulders_chb.pack(anchor=ctk.W)
        back_chb = CheckBox(master, gym_body_parts[4], master.var_back)
        back_chb.pack(anchor=ctk.W)
        biceps_chb = CheckBox(master, gym_body_parts[5], master.var_biceps)
        biceps_chb.pack(anchor=ctk.W)
        triceps_chb = CheckBox(master, gym_body_parts[6], master.var_triceps)
        triceps_chb.pack(anchor=ctk.W)
        forearm_chb = CheckBox(master, gym_body_parts[7], master.var_forearm)
        forearm_chb.pack(anchor=ctk.W)

    @staticmethod
    def GymListForFile(master : object, training_list : list) -> None:
        """Přidá k listu dat specifické informace o tréninku typu posilovna pro zapsání dat do 
        tréninkové databáze."""
        training_list.extend([master.var_time.get(), master.var_legs.get(), master.var_core.get(),
                                master.var_breast.get(), master.var_shoulders.get(),
                                master.var_back.get(), master.var_biceps.get(),
                                master.var_triceps.get(), master.var_forearm.get()])
        return training_list
    
    @staticmethod
    def verifyGym (master : object) -> bool:
        """Ověří vstupy posilovny při zadávání nového tréninku."""
        return True # zatím netřeba ošetřovat
    
    @staticmethod
    def gymPartsFiltrator(master : object, gym_parts_filter :list) -> list:
        """Vyfiltruje posilovnu podle odcvičených částí."""
        # vytvoření pole s názvy zvolených sportů ve filtru
        strings_to_find = []
        for i in range(len(gym_body_parts)):
            if gym_parts_filter[i] == 1:
                strings_to_find.append(gym_body_parts[i])
        # cyklus přes tréninky
        filtered = []
        for training in master.filtered_data:
            if training.sport == sport_list[0]: # výběr posilovacích tréninků
                # každé slovo ze strings_to_find se zkusí najít v odcvičených sportech tréninku
                for i in range(len(strings_to_find)):
                    found = training.practicedParts.find(strings_to_find[i])
                    if found >= 0:
                        filtered.append(training)
            else:
                # pokud se nejedná o posilovnu, přidá se vždy
                filtered.append(training)
        return filtered

    def updateGymGUI (master : object, training : object) -> None:
        """Vytvoří widgety v okně pro úpravu tréninků v Overview, pokud se vybere trénink posilovna."""
        master.var_leg = IntVar()
        master.var_core = IntVar()
        master.var_breast = IntVar()
        master.var_shoulders = IntVar()
        master.var_back = IntVar()
        master.var_biceps = IntVar()
        master.var_triceps = IntVar()
        master.var_forearm = IntVar()
        leg_chb = CheckBox(master, gym_body_parts[0], master.var_leg)
        leg_chb.grid(column = 0, row = master.next_row)
        leg_chb.configure(width=master.box_width)
        core_chb = CheckBox(master, gym_body_parts[1], master.var_core)
        core_chb.grid(column = 1, row = master.next_row)
        core_chb.configure(width=master.box_width)
        breast_chb = CheckBox(master, gym_body_parts[2], master.var_breast)
        breast_chb.grid(column = 2, row = master.next_row)
        breast_chb.configure(width=master.box_width)
        shoulder_chb = CheckBox(master, gym_body_parts[3], master.var_shoulders)
        shoulder_chb.grid(column = 3, row = master.next_row)
        shoulder_chb.configure(width=master.box_width)
        back_chb = CheckBox(master, gym_body_parts[4], master.var_back)
        back_chb.grid(column = 0, row = master.next_row+1)
        back_chb.configure(width=master.box_width)
        biceps_chb = CheckBox(master, gym_body_parts[5], master.var_biceps)
        biceps_chb.grid(column = 1, row = master.next_row+1)
        biceps_chb.configure(width=master.box_width)
        triceps_chb = CheckBox(master, gym_body_parts[6], master.var_triceps)
        triceps_chb.grid(column = 2, row = master.next_row+1)
        triceps_chb.configure(width=master.box_width)
        forearm_chb = CheckBox(master, gym_body_parts[7], master.var_forearm)
        forearm_chb.grid(column = 3, row = master.next_row+1)
        forearm_chb.configure(width=master.box_width)
        master.var_leg.set(Sport.hasAttribute(training, "leg", 0))
        master.var_core.set(Sport.hasAttribute(training, "core", 0))
        master.var_breast.set(Sport.hasAttribute(training, "breast", 0))
        master.var_shoulders.set(Sport.hasAttribute(training, "shoulders", 0))
        master.var_back.set(Sport.hasAttribute(training, "back", 0))
        master.var_biceps.set(Sport.hasAttribute(training, "biceps", 0))
        master.var_triceps.set(Sport.hasAttribute(training, "triceps", 0))
        master.var_forearm.set(Sport.hasAttribute(training, "forearm", 0))
        master.specific_widgets = [leg_chb, core_chb, breast_chb, shoulder_chb, back_chb, biceps_chb, triceps_chb, forearm_chb]
        master.next_row = master.next_row + 2

    def updateGymData (master : object) -> None:
        """Přidá do listu self.main_values hodnoty specifické pro trénink posilovna."""
        master.main_values.extend([master.var_leg.get(), master.var_core.get(), master.var_breast.get(), master.var_shoulders.get(), master.var_back.get(), master.var_biceps.get(), master.var_triceps.get(), master.var_forearm.get()])

    def getGymTrainings (master : object) -> list:
        """Vrátí list tréninků typu posilovna."""
        gym_trainings = []
        for training in master.trainings:
            if training.sport == sport_list[0]:
                gym_trainings.append(training)
        return gym_trainings
    
    def makeGymContent (trainings : list) -> list:
        """Vytvoří list jednotlivých odtrénovaných částí těla."""
        practiced_parts = []
        parts_dict = {}
        colors = []
        for training in trainings:
            if training.practicedParts != unknown_text:
                parts = training.practicedParts.split(", ")
                practiced_parts.extend(parts)
        for part in practiced_parts:
            if part in parts_dict:
                parts_dict[part] = parts_dict[part] + 1
            else:
                parts_dict[part] = 1
                colors.append(pie_chart_palette[part])
        legend_list = parts_dict.keys()
        count_list = parts_dict.values()
        return [legend_list, count_list, colors]