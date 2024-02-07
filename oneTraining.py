#importy knohven
from datetime import date
#importy souborů
from configuration import sport_list, free_day
from sports.setSport import SetSport

class OneTraining ():
    """Třída pro vytvoření instance jednoho tréninku z dat v souboru.
    load - možnost načíst data ze souboru -> trénink pak má všechny svoje vlastnosti, které se o něm ukládají
    save - ..."""
    def __init__(self, operation = "", file_line = ""):
        if operation == "load":
            self._unlockTheData(file_line)
        elif operation == "save":
            ... #TODO předělat ukládání tréninků do objektů


    def _unlockTheData(self, file_line):
        """Funkce rozklíčuje data ze souboru a přiřadí je objektu."""
        # rozdělení řádku ze souboru na jednolivé údaje
        data_list = self._separateData(file_line)

        # uložení data tréninku
        self.date = data_list[0]

        #rozdělení tréninku podle sportu
        self.sport = SetSport.whichSport(data_list[1])

        # rozklíčuje a přiřadí data jako vlastnosti tréninku.
        SetSport.findData(self, data_list)

    def trainingDateBetween(self, first_date : date, second_date : date) -> bool:
        """Rozhodne, zda je datum mezi zadanými datovými hranicemi VČETNĚ."""
        date_list = self.date.split(". ")
        self.real_year = int(date_list[2]) + 2000
        self.real_date = date(self.real_year, int(date_list[1]), int(date_list[0]))
        if first_date <= self.real_date <= second_date:
            between = True
        else:
            between = False
        return between 
    
    def setPlanData (self, sport : str, details : tuple) -> None:
        """Nastaví tréninku data zadané uživatelem v náhledu tréninků."""
        self.date = None
        self.sport = sport
        self.time = details[0]
        SetSport.plan_getSportData(self, details)

    def makeFreeDay (self) -> None:
        """Vytvoří trénink, který reprezentuje volný den."""
        self.date = None
        self.sport = free_day


    def _separateData(self, data_line):
        """Rozdělení dat z řádku na jednotlivé údaje."""
        data_list = data_line.split(" / ")
        del data_list[-1]
        return data_list
