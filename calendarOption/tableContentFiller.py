#import knihoven
import calendar
from tkinter import *
from configuration import trainings_path, cycle_plans_path, single_plans_path, colors
from datetime import date
from icecream import ic
# importy osuborů
from oneTraining import OneTraining
from calendarOption.oneCycleTraining import OneCycleTraining
from calendarOption.oneSingleTraining import OneSingleTraining
from calendarOption.ghostTraining import GhostTraining
from general import General

class TabelContentFiller ():
    """Třída pro plnění kalendáře daty pro zvolený měsíc."""
    def __init__(self, date : tuple):
        self.date = date
        # první a poslední den zobrazený v aktuálním kalendáři
        self.first_date = self._firstDate()
        self.last_date = self._lastDate()
        # list s kalendářními daty pro jednotlivé framy
        self.dates_list = self._datesDayList()
        # listy tréninků
        self.trainings = self._loadTrainings()
        self.cycle_plans = self._loadCyclePlan()
        self.single_plans = self._loadSinglePlan()

    def datesToLabelsConfig(self, frame_list : list, date_list : list) -> None:
        """Metoda pro přidání textu s datem do každého labelu -> framu kalendáře."""
        # cyklus přes framy
        for i in range(len(frame_list)):
            frame_list[i].label.configure(text = date_list[i])
            frame_list[i].configure(fg_color = colors["dark-gray"])

    def displayTrainingWidget(self, frame_list : tuple) -> None:
        """Metoda pro zobrazení widgety s tréninkem v daném dni v kalendáři."""
        # vymazaní předchozího obsahu v kalendáři
        for frame in frame_list:
            for strip in frame.strips:
                strip.destroy()
            frame.strips = []
        # vykreslení stripů s tréninky v jednotlivých dnech
        self._renderActivities(frame_list, self.trainings)
        # vykreslední tréninkových plánů
        self._displayPlans(frame_list)

    def _displayPlans (self, frame_list : tuple) -> None:
        """Zobrazí naplánované tréninky z tréninkových plánů."""
        self._dispCyclePlans(frame_list)
        self._dispSinglePlans(frame_list)
        #TODO ostatní typy plánů
        self._dispCycleFreeDays(frame_list)
        #TODO ostatní typy volných dní

    def _dispCyclePlans (self, frame_list : tuple) -> None:
        """Zobrazí v kalendáři naplánované tréninky pocházející z cyklických tréninkových plánů."""
        for plan in self.cycle_plans:
            # pokud nesedí plán do data, celý tréninkový plán se přeskočí
            if self._cyclePlanInPast(): continue
            if not self._intersectDates(plan): continue
            # vypočet data začátku nového cyklu tréninkového plánu nejblíže před začátkem zobrazovaného období a po konci zobrazovaného období
            first_cycle = self._nearestDateToStart(plan)
            last_cycle = self._nearestDateToEnd(plan)
            # vygenerování plánovaných tréninků do kalendáře.
            ghost_trainings = self._GhostTrainings(plan, first_cycle, last_cycle, "training")
            # vykreslení tréninků
            self._renderActivities(frame_list, ghost_trainings)
            # self._renderFreeDay(frame_list, ghost_free_days)

    def _dispCycleFreeDays (self, frame_list : tuple) -> None:
        """Zobrazí v kalendáři naplánované volné dny pocházející z cyklických tréninkových plánů."""
        for plan in self.cycle_plans:
            # pokud nesedí plán do data, celý tréninkový plán se přeskočí
            if self._cyclePlanInPast(): continue
            if not self._intersectDates(plan): continue
            # vypočet data začátku nového cyklu tréninkového plánu nejblíže před začátkem zobrazovaného období a po konci zobrazovaného období
            first_cycle = self._nearestDateToStart(plan)
            last_cycle = self._nearestDateToEnd(plan)
            # vygenerování plánovaných tréninků do kalendáře.
            ghost_free_days = self._GhostTrainings(plan, first_cycle, last_cycle, "fd")
            # vykreslení tréninků
            # self._renderActivities(frame_list, ghost_trainings)
            self._renderFreeDay(frame_list, ghost_free_days)

    def _dispSinglePlans (self, frame_list : tuple) -> None:
        """Zobrazí v kalendáři tréninky pocházející z jednoduchých tréninkových plánů."""
        for plan in self.single_plans:
            if self._singlePlanInPast(plan): continue
            if not self._intersectDates(plan): continue
            trainings = self._cutOffForeignTrains(plan.all_trainings)
            self._renderActivities(frame_list, trainings)

    def _renderActivities (self, frame_list : tuple, strips_to_render : list) -> None:
        """Vykreslí stripy tréninků do jednotlivých framů v kalendáři."""
        for activity in strips_to_render:
            index_of_frame = self._frameIndexOfDay(activity.real_date)
            frame_list[index_of_frame].createStrip(activity)

    def _renderFreeDay (self, frame_list : tuple, free_days_to_render : list) -> None:
        """VYkreslí labely jednotlivých dnů do kalendáře, pokud už dny nejsou obsazeny aktivitou."""
        for day in free_days_to_render:
            index_of_frame = self._frameIndexOfDay(day.real_date)
            if not frame_list[index_of_frame].strips:
                frame_list[index_of_frame].createFreeDay()

    def _cyclePlanInPast (self) -> bool:
        """Zkontroluje, zda je trénink zobrazené období v minulosti, pokud ano, tréninkové plány se
        nezobrazují, pokud ne nebo část ne, plán se zobrazí."""
        if date.today() > self.last_date:
            return True
        return False
    
    def _singlePlanInPast (self, plan : object) -> bool:
        """Zkontroluje, zda ještě nějaký trénink z plánu aktuální, pokud se jedná o minulost, přeskočí se."""
        if date.today() > plan.end_date:
            return True
        return False
    
    def _cutOffForeignTrains (self, trainings : list) -> list:
        """Vystřihne z pole tréninků tréninky, které neodpovídají zobrazenému období. Vrátí list tréninků ve zobrazeném období."""
        right_trains = []
        for training in trainings:
            if General.dateBetween(training.real_date, self.first_date, self.last_date):
                right_trains.append(training)
        return right_trains

    def _intersectDates (self, train_plan : object) -> bool:
        """Rozhodne, zda se tréninkový plán a zobrazené období v kalendáři časově protínají.
        Ano - tréninky se vypíší, Ne - tréninkový plán se přeskočí.""" 
        if self.last_date < train_plan.start_date:
            return False
        elif self.first_date > train_plan.end_date:
            return False
        return True

    def _nearestDateToStart (self, train_plan : object) -> int:
        """Najde nejbližší datum začátku nového cyklu tréninkového plánu před prvním dnem 
        zobrazeným v kalendáři a vrátí jeho index ve slovníku počátečních dat cyklů objektu."""
        start_date = 1
        for date in train_plan.next_cycle:
            if train_plan.next_cycle[date] > self.first_date:
                start_date = date - 1
                if start_date == 0: # protože když to začíná uprostřed zobrazované části, tak by to hodilo index 0
                    start_date = 1
                return start_date
        return 1

    def _nearestDateToEnd (self, train_plan : object) -> int:
        """Najde nejbližší datum začátku dalšího cyklu tréninkového plánu po podlením datu
        zobrazovaného období v kalendáří a vrátí jeho index."""
        for end_date in train_plan.next_cycle:
            if train_plan.next_cycle[end_date] > self.last_date:
                return end_date - 1 #TODO, tady vyřešit - 1
        # pokud by cyklus končil dřív než zobrazovaná doba, vrátí se poslední index
        return len(train_plan.next_cycle)
    
    def _GhostTrainings (self, train_plan : object, first_cycle : int, last_cycle : int,
                         train_or_fd  : str) -> list:
        """Zavolá třídu GhostTrainings, která vytvoří list tréninků a lsit volných dní podle 
        tréninkového plánu pro dané období. Vrátí 2 listy.\n
        Vstupy: (tréninkový plán, počáteční cyklus, koncový cyklus, ("train" / "fd") který 
        ist to vrátí.)"""
        ghost_training = GhostTraining(train_plan, first_cycle, last_cycle)
        activity_list = ghost_training.getGhostActivList(train_or_fd)
        # free_days_list = ghost_training.getFreeDaysList()
        activity_list = self._ghostTermCheck(activity_list)
        # free_days_list = self._ghostTermCheck(free_days_list)
        activity_list = self._ghostTermInPast(activity_list)
        # free_days_list = self._ghostTermInPast(free_days_list)
        return activity_list
        
    def _ghostTermCheck(self, ghost_trainings : list) -> list:
        """Kontroloní funkce, pokud v listu tréninků skončí trénink, který by nebyl ve 
        zobrazovaném období, tak se vyřadí."""
        trimmed_ghost_trains = []
        for ghost in ghost_trainings:
            # pokud trénink není v rozmezí zobrazovaných dní, odmaže se z listu tréninků
            if self.first_date <= ghost.real_date <= self.last_date:
                trimmed_ghost_trains.append(ghost)
        return trimmed_ghost_trains
    
    def _ghostTermInPast(self, ghost_activities : list) -> list:
        """Pokud je aktivita v minulosti, vyřadí se z list aktivit."""
        today = date.today()
        future_activities = []
        for activity in ghost_activities:
            # pokud je už po datu, kdy aktivita měla proběhnout, odmaže se z listu aktivit
            if not activity.real_date < today:
                future_activities.append(activity)
        return future_activities

    def _datesDayList (self) -> list:
        """Metoda vrátí list dat pro každý den (čtvereček) z kalendáře."""
        # tuple s hodnotou prvního dne v týdnu zadaného měsíce
        # a hodnotou počtu dní v měsíci
        key_dates = self._firstDay_NumOfDays(self.date)
        # získání počtu dní předchozího měsíce
        prev_month_date = self._prevMonth(self.date)
        # tuple s key_dates predchozího měsíce
        prev_month_key_dates = self._firstDay_NumOfDays(prev_month_date)
        next_month_date = self._nextMonth(self.date)

        # deklarace listu pro hodnoty dat
        dates_list = [None] * 42
        # naplnění listu daty aktuálního měsíce 
        # (od hodnoty dne kterým měsíc začíná -> počet dní krát)
        date_increment = 1
        for i in range(key_dates[0], key_dates[1] + key_dates[0]):
            dates_list[i] = str(date_increment)
            date_increment = date_increment + 1
        # naplnění hodnotami po skončení měsíce
        date_increment = 1
        for j in range(key_dates[0] + key_dates[1], 42):
            string = str(date_increment) + ". " + str(next_month_date[1]) + "."
            dates_list[j] = string
            date_increment = date_increment + 1
        # naplnění daty před začátkem zvoleného měsíce
        date_increment = prev_month_key_dates[1] - key_dates[0] + 1 # poč. dní předch. měsíce - den začátku tohoto měsíce + 1
        for k in range(0, key_dates[0]):
            string = str(date_increment) + ". " + str(prev_month_date[1]) + "."
            dates_list[k] = date_increment
            date_increment = date_increment + 1
        return dates_list

    def _firstDay_NumOfDays (self, date : tuple) -> int:
        "Funkce zjistí, jaký den v týdnu je 1. v měsíci a kolik má měsíc dní."
        return calendar.monthrange(date[0], date[1])


    def _prevMonth (self, date : tuple) -> list:
        """Posune nastavený měsíc o jeden zpět."""
        month = date[1]
        year = date[0]
        if month >= 2:
            month = month - 1
        else:
            month = 12
            year = year - 1
        date = (year, month)
        return date
    
    def _nextMonth (self, date : tuple) -> list:
        """Posune nastavený měsíc o jeden dopředu."""
        month = date[1]
        year = date[0]
        if month <= 11:
            month = month + 1
        else:
            month = 1
            year = year + 1
        date = (year, month)
        return date
        
    def _loadTrainings(self) -> list:
        """Metoda pro načtení tréninků pomocí OneTraining z databáze.
        Vrátí list tréninků"""
        # načtení všech dat do pole po jednotlivých řádcích
        lines = General.loadLinesFromFile(trainings_path)
        # vytvoření objektů jednotlivých tréninků
        trainings = []
        for one_line in lines:
            one_training = OneTraining(self, "load", one_line)
            # vyhodnocení, zda trénink je v tomto kalendáři vidět
            between = one_training.trainingDateBetween(self.first_date, self.last_date)
            if between:
                trainings.append(one_training)
        return trainings
    
    def _loadCyclePlan (self) -> list:
        """Metoda načte cyklický tréninkový plán pomocí OneCycleTraining z databáze cyklického plánu.
        Vrátí načtená data tréninkového cyklu jako list."""
        # pokud není v databázi žádný plán -> ukončí se
        if General.isFileEmpty(cycle_plans_path):
            return []
        # načtení souboru po jednotlivých řádcích
        lines = General.loadLinesFromFile(cycle_plans_path)
        # vytvoření listů s daty pro jeden tréninkový plán
        plans_data = self._compilePlanData(lines)
        # list s objekty jednotlivých plánů
        cycle_plans = self._makeCyclePlans(plans_data)
        return cycle_plans
    
    def _loadSinglePlan (self) -> list:
        """Metoda načte cyklický tréninkový plán pomocí OneSingleTraining z databáze jednocuchého tréninkového plánu.
        Vrátí načtená data tréninkového culku jako list."""
        # pokud v databázi nic není -> přeskočí se
        if General.isFileEmpty(single_plans_path):
            return []
        lines = General.loadLinesFromFile(single_plans_path)
        # vytvoření listů s daty pro jeden tréninkový plán
        plans_data = self._compilePlanData(lines)
        # list s objekty jednotlivých plánů
        single_plans = self._makeSinglePlans(plans_data)
        return single_plans
    
    def _compilePlanData (self, file_lines : list) -> list:
        """Vrátí jeden list zpracovaných dat vytvořených z načtených řádků z databáze 
        cyklického tréninkového plánu."""
        cycle_plans = [[]] # list plánů
        i = 0 # proměnná indexů listu
        for one_line in file_lines: # cyklus přes řádky ze souboru
            one_line = one_line.replace("\n", "") # vymazání odřádkovacích znaků
            if one_line == ";": # pokud je to dělící řádek
                i = i + 1 # zvýší se index listu
                cycle_plans.append([]) # přidání listu na konec (velkého) listu, pro další tréninkový plán
            else:
                cycle_plans[i].append(one_line)
        del cycle_plans [-1] # odstranění podleníhoo indexu, který se vždy udělá navíc
        return cycle_plans
    
    def _setUndefinedItems (self, plan_data : list) -> list:
        """Místo nazadaných hodnot vloží string, který je nastavený na vypsání nazadané hodnoty pro uživatele."""
        for i in range(len(plan_data)):
            plan_data[i] = General.setStringForUndefined(plan_data)
        return plan_data
    
    def _makeCyclePlans (self, plans_data : list) -> list:
        """Ze zpracovaných dat z databáze cyklického tréninkového plánu vytvoří list objektů
        jednotlivých tréninkových plánu. Vrátí list cyklických tréninkových plánů."""
        cycle_plans = []
        for plan_data in plans_data:
            one_plan = OneCycleTraining(plan_data)
            cycle_plans.append(one_plan)
        return cycle_plans
    
    def _makeSinglePlans (self, plans_data : list) -> list:
        """Ze zpracovaných dat z databáze jednoduchého tréninkového plánu vytvoří list objektů jednotlivých tréninkových plánu. Vrátí list jednoduchých tréninkových plánů."""
        single_plans = []
        for plan_data in plans_data:
            one_plan = OneSingleTraining(plan_data)
            single_plans.append(one_plan)
        return single_plans
            
    def _frameIndexOfDay (self, date_of_training : date) -> int:
        """Metoda vrátí index framu se dnem, do kterého se má widgeta zobrazit."""
        training_date = (date_of_training.year, date_of_training.month)
        prev_month_date = self._prevMonth(self.date) # data předchozího měsíce
        next_month_date = self._nextMonth(self.date) # data přístího měsíce
        key_dates = self._firstDay_NumOfDays(self.date) # klíčové údaje o zvoleném měsíci
        key_dates_prev = self._firstDay_NumOfDays(prev_month_date) # klíčové údaje o předchozím měsíci
        # pokud je trénink v měsíci který odpovídá vybranému měsíci
        if training_date == self.date:
            frame_index = key_dates[0] + date_of_training.day - 1
        # pokud je trénink v předchozím měsíci, ale ve viditelné oblasti
        elif training_date == prev_month_date:
            first_date = self._firstDate()  # první den zobrazený v kalendáři
            # frame_index = key_dates_prev[1] - first_date.day - 1
            frame_index = date_of_training.day - first_date.day
        # pokud je trénink v následujícím měsíci, ale ve viditelné oblasti
        elif training_date == next_month_date:
            frame_index = key_dates[0] + key_dates[1] + date_of_training.day - 1
        return frame_index

    def _firstDate (self) -> date:
        """Vrátí datum prvního dne zobrazovaného v tabulce."""
        # získání dat
        key_dates = self._firstDay_NumOfDays(self.date)
        prev_month_date = self._prevMonth(self.date)
        prev_key_dates = self._firstDay_NumOfDays(prev_month_date)
        # datum prvního dne v kalendáři
        if key_dates[0] == 0:
            first_date = date(self.date[0], self.date[1], 1)
        else:
            day = prev_key_dates[1] + 1 - key_dates[0]
            first_date = date(prev_month_date[0], prev_month_date[1], day)
        return first_date
    
    def _lastDate (self) -> date:
        """Vrátí datum posledního dne zobrazeného v kalendáří."""
        # získání dat
        key_dates = self._firstDay_NumOfDays(self.date)
        next_month_date = self._nextMonth(self.date)
        # datum posledního dne v kalendáři
        day = 42 - key_dates[0] - key_dates[1]
        last_date = date(next_month_date[0], next_month_date[1], day)
        return last_date
