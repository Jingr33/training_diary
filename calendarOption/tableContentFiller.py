#import knihoven
import calendar
from tkinter import *
from configuration import trainings_path, cycle_plans_path
from datetime import date
# importy osuborů
from oneTraining import OneTraining
from calendarOption.oneCycleTraining import OneCycleTraining
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
        self.trainings = self._loadTrainingns()
        self.cycle_plans = self._loadCyclePlan()

    def datesToLabelsConfig(self, frame_list : list, date_list : list) -> None:
        """Metoda pro přidání textu s datem do každého labelu -> framu kalendáře."""
        # cyklus přes framy
        for i in range(len(frame_list)):
            frame_list[i].label.configure(text = date_list[i])

    def displayTrainingWidget(self, frame_list : tuple) -> None:
        """Metoda pro zobrazení widgety s tréninkem v daném dni v kalendáři."""
        # vymazaní předchozího obsahu v kalendáři
        for frame in frame_list:
            for strip in frame.strips:
                strip.destroy()
        # vykreslení stripů s tréninky v jednotlivých dnech
        self._renderActivities(frame_list, self.trainings)
        # vykreslední tréninkových plánů
        self._displayPlans(frame_list)

    def _renderActivities (self, frame_list : tuple, strips_to_render : list) -> None:
        """Vykreslí stripy tréninků do jednotlivých framů v kalendáři."""
        for training in strips_to_render:
            index_of_frame = self._frameIndexOfDay(training.real_date)
            frame_list[index_of_frame].createStrip(training)

    def _displayPlans (self, frame_list : tuple) -> None:
        """Zobrazí naplánované tréninky z tréninkových plánů."""
        self._dispCyclePlans(frame_list)

    def _dispCyclePlans (self, frame_list : tuple) -> None:
        """Zobrazí v kalendáři naplánované tréninky pocházející z cyklickýxh tréninkových plánů."""
        for plan in self.cycle_plans:
            # pokud nesedí plán do data, celý tréninkový plán se přeskočí
            if not self._intersectDates(plan):
                continue
            # vypočet data začátku nového cyklu tréninkového plánu nejblíže před začátkem zobrazovaného období a po konci zobrazovaného období
            first_cycle = self._nearestDateToStart(plan)
            last_cycle = self._nearestDateToEnd(plan)
            # vygenerování plánovaných tréninků do kalendáře.
            ghost_trainings = self._GhostTrainings(plan, first_cycle, last_cycle)
            # vykreslení tréninků
            self._renderActivities(frame_list, ghost_trainings)

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
    
    def _GhostTrainings (self, train_plan : object, first_cycle : int, last_cycle : int) -> list:
        """Zavolá třídu GhostTrainings, která vytvoří list tréninků podle tréninkového plánu pro dané období"""
        ghost_training = GhostTraining(train_plan, first_cycle, last_cycle)
        train_list = ghost_training.getGhostTrainList()
        train_list = self._ghostTremCheck(train_list)
        return train_list
    
    def _ghostTremCheck(self, ghost_trainings : list) -> list:
        """Kontroloní funkce, pokud v listu tréninků skončí trénink, který by nebyl ve 
        zobrazovaném období, tak se vyřadí."""
        for ghost in ghost_trainings:
            # pokud trénink není v rozmezí zobrazovaných dní, odmaže se z listu tréninků
            if not self.first_date <= ghost.real_date <= self.last_date:
                ghost_trainings.remove(ghost)
        return ghost_trainings

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
        
    def _loadTrainingns(self) -> list:
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
        Vrátí načtená data tréninkového cyklu jak list."""
        # pokud není v databázi žádný plán -> ukončí se
        if General.isFileEmpty(cycle_plans_path):
            return []
        # načtení souboru po jednotlivých řádcích
        lines = General.loadLinesFromFile(cycle_plans_path)
        # vytvoření listů s daty pro jeden tréninkový plán
        plans_data = self._compileCyclePlanData(lines)
        # list s objekty jednotlivých plánů
        cycle_plans = self._makeCyclePlans(plans_data)
        return cycle_plans
    
    def _compileCyclePlanData (self, file_lines : list) -> list:
        """Vrátí jeden list zpracovaných dat vytvořených z načtených řádků z databáze 
        cyklického tréninkového plánu."""
        cycle_plans = [[]] # list plánů
        i = 0 # proměnný indexů listu
        for one_line in file_lines: # cyklus přes řádky ze souboru
            one_line = one_line.replace("\n", "") # vymazání odřádkovacích znaků
            if one_line == ";": # pokud je to dělící řádek
                i = i + 1 # zvýší se index listu
                cycle_plans.append([]) # přidání listu na konec (velkého) listu, pro další tréninkový plán
            else:
                cycle_plans[i].append(one_line)
        del cycle_plans [-1] # odstranění podleníhoo indexu, který se vždy udělá navíc
        return cycle_plans
    
    def _makeCyclePlans (self, plans_data : list) -> list:
        """Ze zpracovaných dat z databáze cyklického tréninkového plánu vytvoří list objektů
        jednotlivých tréninkových plánu. Vrátí list cyklických tréninkových plánů."""
        cycle_plans = []
        for plan_data in plans_data:
            one_plan = OneCycleTraining(plan_data)
            cycle_plans.append(one_plan)
        return cycle_plans
            
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
            frame_index = key_dates_prev[1] - first_date.day - 1
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
