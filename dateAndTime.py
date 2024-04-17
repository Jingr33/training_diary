# import knihoven
from datetime import datetime, date
from icecream import ic


class DateAndTime ():
    """Třída pro práci a datem a časem."""
    def __init__(self, master : object):
        self.master = master

    def getDuration(self, then : datetime, now : datetime) -> dict:
        """Vrátí slovník hodnot trvání mezi dvěma okamžiky (počet let a zbývajících dní a zbývajících hodin atd.)"""
        duration = now - then
        duration_in_s = duration.total_seconds()
        years = divmod(duration_in_s, 31536000)
        days = divmod(years[1],86400)
        hours = divmod(days[1],3600)
        minutes = divmod(hours[1],60)
        seconds = minutes[1]
        return {
            "year" : int(years[0]),
            "day" : int(days[0]), 
            "hour" : int(hours[0]), 
            "minute" : int(minutes[0]), 
            "second" : int(seconds),
        }
    
    def getDurationInStr (self, older_datetime, now = datetime.now()) -> str:
        """Vrátí časové období mezi dvěma okamžiky ve formátu stringu (do labelu)."""
        if isinstance(now, date) and not isinstance(now, datetime): # převedení date na datetime
            now = datetime.combine(now, datetime.min.time())
        periods = self.getDuration(older_datetime, now)
        string = ""
        for key in periods:
            if periods[key]:
                string = "{0}, {1} {2}".format(string, periods[key], self.periodInflection(periods[key], key))
        string = string[2:] # odstraní přebytečnou čárku na začátku
        return string

    def periodInflection (self, count : int, type_of_period : str) -> str:
        """Skloní název časového období podle jeho množství (rok, den, hodina, minuta, sekunda)."""
        for_onetime = {"year" : "rokem",
                       "day" : "dnem",
                       "hour" : "hodinou",
                       "minute" :  "minutou",
                       "second" :  "sekundou",
                       }
        for_severaltimes = {"year" : "lety",
                       "day" : "dny",
                       "hour" : "hodinami",
                       "minute" :  "minutami",
                       "second" :  "sekundami",
                       }
        if count == 1:
            return for_onetime[type_of_period]
        return for_severaltimes[type_of_period]

    def getDaysDuration (self, start_date : date, end_date : date) -> int:
        """Vrátí počet dní (int) meti počátěčním a koncovým datem."""
        return abs((end_date - start_date).days)