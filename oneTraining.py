#importy knohven
from datetime import date
#importy souborů
from sports.setSport import SetSport
from globalVariables import increaseID, training_id
from configuration import free_day, trainings_path, unknown_text
from sports.setSport import SetSport
from general import General

class OneTraining ():
    """Třída pro vytvoření instance jednoho tréninku z dat v souboru.
    load - možnost načíst data ze souboru -> trénink pak má všechny svoje vlastnosti, které se o něm ukládají
    save - ..."""
    def __init__(self, master : object, operation = "", file_line = "", data_list = ""):
        self.master = master
        if operation == "load":
            self._unlockTheData(file_line)
        elif operation == "save":
            self._getTrainingToFile(data_list)

    def _unlockTheData(self, file_line):
        """Funkce rozklíčuje data ze souboru a přiřadí je objektu."""
        # rozdělení řádku ze souboru na jednolivé údaje
        print(file_line)
        data_list = self._separateData(file_line)
        # nastavení od tréninku
        self._setTrainingID()
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

    def _setTrainingID (self) -> None:
        """Metoda nastaví tréninku id jako jeho vlastnost."""
        increaseID(training_id)
        self.id = training_id
    
    def _getTrainingToFile (self, data_list : list) -> None:
        """Uloží data do souboru ve správném formátu."""
        calendar_date = data_list[0]
        self.sport = data_list[1]
        self.date = self._editDateFormat(calendar_date) # úprava zápisu data
        training_list = [self.date, self.sport]
        SetSport.fillListForFile(self.master, training_list)
        training_list = self._isSetted(training_list)# při nezadání vstupu přidá neuvedeno
        prepared_string = General.prepareString(training_list)
        self._writeToFile(prepared_string)

    def _editDateFormat(self, original_date :str) -> str:
        """Metoda pro přepsaní data z formátu tkinterového 
        kalendáře do formátu českého zápisu data."""
        mmddyy = original_date.split("/")# převedení údajů (měsíc, datum, rok) do listu
        for i in range(len(mmddyy)):  # přidání 0 před číslo, pokud je menší než 10
            if int(mmddyy[i]) < 10:
                mmddyy[i] = "0" + mmddyy[i]
        # vytvoření stringu s českým datem
        formated_date = mmddyy[1] + ". " + mmddyy[0] + ". " + mmddyy[2]
        return formated_date

    def _writeToFile (self, string):
        """Metoda pro zapsání dat do souboru."""
        with open(trainings_path, 'a') as f:  
            f.write(string + " / \n")

    def _isSetted (self, list : list) -> list:
        """Pro nezadané položky listu ("") zadá do proměnné, že údaj nebyl uveden. """
        for i in range(len(list)):
            list[i] = self._setUnknow(list[i])
        return list

    def _setUnknow (self, entry : str) -> None:
        """Nastavý zadaný parametr na neuvedený, pokud je užvatelský vstup prázdný."""
        if entry:
            return entry
        else:
            return unknown_text
