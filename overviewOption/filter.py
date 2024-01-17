# importy souborů
from configuration import sport_list

class Filter():
    """Filtruje tréninky podle vybraných parametrů."""
    def __init__(self, trainings, date_filter, sport_filter, time_filter):
        self.trainings = trainings

        # vyfiltrování podle filtrovaných sportů
        self.filtered_data = self._sportFiltrator(sport_filter)

        #TODO vyfiltrování dat podle data
        self._dataFiltrator(date_filter)

        # vyfiltrování data podle času
        self.filtered_data = self._timeFiltrator(time_filter)

        #TODO ostatní filtry

    
    def getFilteredData(self):
        return self.filtered_data
    
    def _sportFiltrator(self, sport_filter):
        """Vyfiltruje data podle sportu."""
        # převede číselné hodnoty z filtru do slovní podoby
        desired_sports = []
        i = 0
        for sport in sport_filter:
            if int(sport) == 1:
                desired_sports.append(sport_list[i])
            i = i + 1

        # pokud se sport rovná sportu ve filtru, trénink se vybere
        filtered = []
        for training in self.trainings:
            for sport in desired_sports:
                if training.sport == sport:
                    filtered.append(training)
        return filtered
    
    def _dataFiltrator(self, date_filter):
        """Vyfiltruje data podle datumu."""
        ... 
        #TODO


    def _timeFiltrator(self, time_filter):
        """Vyfiltruje data podle času."""
        filtered = []
        for training in self.filtered_data:
            if (int(training.time) >= int(time_filter[0])) and (int(training.time) <= int(time_filter[1])):
                filtered.append(training)
        return filtered
        
