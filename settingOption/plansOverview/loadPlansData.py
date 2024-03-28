#import knihoven
from icecream import ic
#import souborů
from general import General
from configuration import cycle_plans_path, single_plans_path


class LoadPlansData ():
    """Nečítá a ukládá data o tréninkových plánech načtené z databáze tréninkových plánů (nastavení aplikace -> přehled tréninkových plánů)."""
    def __init__(self, master):
        self.master = master
        self.plan_data = self._loadTrainingPlans()

    def getNumberOfPlans (self) -> int:
        """Vrátí počet všech tréninkových plánů, které by se měli zobrazit v přehledu tréninkových plánů."""
        return len(self.plan_data)
    
    def getTrainingPlansData (self) -> list:
        """Vrátí list informací o všech tréninkových plánech zapsaných v databázi."""
        return self.plan_data
    
    def getOnePlanData (self, index : int) -> list:
        """Vrátí list údajů o jednom tréninkovém plánu. Vstup je index tréninkového plánu."""
        return self.plan_data[index]

    def _loadTrainingPlans (self) -> list:
        """Načte tréninkové plány z databáze, vrátí list informací o nich."""
        file_list = self._loadFileLines()
        cycle_data = self._loadCyclePlans(file_list[0])
        single_data = self._loadSinglePlans(file_list[1])
        plan_data = []
        plan_data.extend(cycle_data)
        plan_data.extend(single_data)
        return plan_data

    def _loadFileLines (self) -> list:
        """Načte data o trénincích z databází."""
        file_list = []
        for plan in (cycle_plans_path, single_plans_path):
            lines = General.loadLinesFromFile(plan)
            for i in range(len(lines)):
                lines[i] = lines[i].replace("\n", "")
            file_list.append(lines)
        return file_list
    
    def _loadCyclePlans (self, lines : list) -> list:
        """Rozklíčuje data z cycle_plan_database.txt a uloží je pro vypsání v přehledu tréninkových plánů."""
        lines = self._selectUsefulLines(lines)
        plan_data = [None] * len(lines)
        i = 0
        for one_line in lines:
            one_date = self._separatePlanData(one_line)
            one_date = self._unlockCycleData(one_date)
            plan_data[i] = one_date
            i = i + 1
        return plan_data

    def _loadSinglePlans (self, lines: list) -> list:
        """Rozklíčuje data ze sigle_plan_databese.txt a uloží je pro vypsání v přehledu tréninkových plánů."""
        lines = self._selectUsefulLines(lines)
        plan_data = [None] * len(lines)
        for i in range(len(lines)):
            one_date = self._separatePlanData(lines[i])
            del one_date[-1] # poslední udaj je prázdný
            one_date = self._unlockSingleData(one_date)
            plan_data[i] = one_date
        return plan_data

    def _selectUsefulLines (self, lines : list) -> list:
        """Vybere pouze užitečné řádky a zbytek vyřadí."""
        useful = [lines[0]]
        for i in range(1, len(lines)):
            if lines[i] == ";" and i + 1 < len(lines):
                useful.append(lines[i+1])
        return useful
    
    def _separatePlanData (self, plan : list) -> list:
        """Rozseká data podle rozdělovače a vrátí listy v listu informací o tréninkových plánech."""
        return General.separateData(plan)
    
    def _unlockCycleData (self, data : list) -> list:
        """Rozklíčuje  data cyklického tréninkového plánu, vrátí list [typ, začátek, další]."""
        plan_data = ["Cyklický", data[0], None]
        if data[1] != "":
            plan_data[2] = "Konec: {0}".format(data[1])
        elif data[2] != "":
            plan_data[2] = "Počet cyklů: {0}".format(data[2])
        return plan_data

    def _unlockSingleData (self, data : list) -> list:
        """Rozklíčuje data jednoduchého tréninkového plánu, vrátí list [první datum, poslední datum]."""
        for i in range(len(data)):
            data[i] = General.stringToDate(data[i])
        data.sort()
        first_date = General.changeDateFormat(data[0])
        last_date = "Konec: {0}".format(General.changeDateFormat(data[-1]))
        return ["Jednoduchý", first_date, last_date]
    