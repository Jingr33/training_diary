#import knihoven
from datetime import date, timedelta
import math
#import souborů
from general import General
from oneTraining import OneTraining


class OneCycleTraining ():
    """Třída pro zpracování dat pro jeden cyklický tréninkový plán. Přijmá list údaji o
    tréninkovém plánu."""
    def __init__(self, plan_data : list):
        self._setMainInfo(plan_data[0]) # zpracuje hlavní informace o plánu
        self._setActivities(plan_data) # vytvoří list tréninků s aktivitami
        self._setDates() # nastavení dat ve formátu date
        self._missingData() # dolní chybějící data
        self.length = self._lengthThroughCycles() # nastavení délky cyklu v dních
        self.next_cycle = self._startNextCycle()

    def _setMainInfo (self, main_data : str) -> None:
        """Zpracuje a uloží data o začátku, konci, počtu cyklů a délce (počtu dní)
        cyklického tréninkového plánu."""
        # rozkouskování řádku na údaje
        data_list = General.separateData(main_data)
        # uložení dat
        self.start = data_list[0]
        self.end = General.checkIfSet(data_list[1])
        self.cycles = General.checkIfSet(data_list[2])
        self.days_length = int(data_list[3]) #délka (počet dní cyklu)

    def _setActivities (self, plan_data) -> None:
        """Zpracuje informace o aktivitách v tréninkovém plánu. Vytvoří plánované tréninky
        a přidá je do listu."""
        self.activities = [None] * (len(plan_data) - 1)
        for i in range(1, len(plan_data)):
            self.activities[i - 1] = OneTraining("load_plan", plan_data[i])

    def _missingData (self) -> None:
        """Pokud některá z informací nebyla zadána, doplní se. (konec, počet cyklů)."""
        if not self.end:
            length = self._lengthThroughCycles()
            self.end_date = self.start_date + timedelta(days = length)
            end_str = str(self.end_date).split("-")
            self.end = end_str[2] + "/" + end_str[1] + "/" + end_str[0]
        if not self.cycles:
            lenght = self._lengthThroughDates()
            self.cycles = math.floor(lenght / self.days_length)

    def _setDates (self) -> int:
        """Vrátí délku trvání tréninkového plánu (počet dní) jako integer."""
        # počáteční datum
        start_list = self.start.split("/")
        self.start_date = date(int(start_list[2]), int(start_list[1]), int(start_list[0]))
        # koncové datum, pokud bylo zadáno
        if self.end:
            end_list = self.end.split("/")
            self.end_date = date(int(end_list[2]), int(end_list[1]), int(end_list[0]))

    def _lengthThroughCycles (self) -> int:
        """Vypočítá délku tréninkového plánu pomocí počtu cyklů."""
        length = int(self.cycles) * int(self.days_length)
        return length
    
    def _lengthThroughDates (self) -> int:
        """Vypočítá dělku tréninkového plánu pomocí počát. a konc. data."""
        return int((self.end_date - self.start_date).days) + 1
    
    def _startNextCycle (self) -> dict:
        """Vytvoří slovník dat, kde klíč je číslo opakování cyklu a hodnota 
        je datum počátečního dne cyklu."""
        cycles_dates = {}
        for i in range(int(self.cycles)):
            cycles_dates[i + 1] = self.start_date + timedelta(days = self.days_length * (i))
        return cycles_dates