# import knihoven
from datetime import date

class General():
    """Třídá základních statických funkcí používaných na hodně místech."""
    @staticmethod
    def checkIntEntry(entry: str) -> bool:
        """Ověří zda je vstupní hodnota int."""
        try:
            int(entry)
            checked = True
        except:
            checked = False
        return checked
    
    @staticmethod
    def checkDateEntry(entry : str) -> bool:
        """Ověří, zda je vstupní hodnota platné datum.
        vstup : dd/mm/yyyy"""
        try:
            date_list = entry.split("/") # rozdělí vstup
            str_day, str_month, str_year = date_list # uloží list do proměnných
            day = int(str_day) # převede na int
            month = int(str_month)
            year = int(str_year)
            entry_date = date(year, month, day) # vytvoří datum
            checked = True
        except:
            checked = False
        return checked
    
    @staticmethod
    def prepareString(list :list) -> str:
        """Připraví string jako jeden řádek zápisu do souboru."""
        line = str(list[1])
        if len(line) >= 2:
            for i in range(2, len(list)):
                line = line + " / " + str(list[i])
        return line