# importy souborů
from configuration import sport_list

class Filter():
    """Filtruje tréninky podle vybraných parametrů."""
    def __init__(self, trainings, date_filter, sport_filter, time_filter):
        self.trainings = trainings

        # vyfiltrování podle filtrovaných sportů
        self.filtered_data = self._sportFiltrator(sport_filter)

        # vyfiltrování podle filtrovaného data
        self.filtered_data = self._dateFiltrator(date_filter)

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

    def _dateFiltrator(self, date_filter):
        """Vyfiltruje data podle datumu."""
        # rozklíčování stringů data do proměnných typu date
        train_date = []
        for training in self.filtered_data:
            train_date_list = training.date.split(". ")
            new_date = "20" + train_date_list[2] + "-" + train_date_list[1] + "-" + train_date_list[0]
            train_date.append(new_date)

        # pokud není filtr nastavený -> filterm údaj projde vždy
        # spodní hranice data (od)
        if date_filter[0] == "":
            bottom_condition = True
            from_date = ""
        else:
            from_date_list = date_filter[0].split("/")
            from_date = "20" + from_date_list[2] + "-" + from_date_list[1] + "-" + from_date_list[0]
            bottom_condition = False

        # horní hranice data (do)
        if date_filter[1] == "":
            top_condition = True
            to_date = ""
        else:
            to_date_list = date_filter[1].split("/")
            to_date = "20" + to_date_list[2] + "-" + to_date_list[1] + "-" + to_date_list[0]
            top_condition = False

        # vytřídění dat podle zadaných mezí
        filtered = []
        j = 0
        for training in self.filtered_data:
            if (((train_date[j] >= from_date) or bottom_condition) 
                and ((train_date[j] <= to_date) or top_condition)):
                filtered.append(training)
            j = j + 1
        return filtered
    
    def _timeFiltrator(self, time_filter):
        """Vyfiltruje data podle času."""
        filtered = []
        for training in self.filtered_data:
            if (int(training.time) >= int(time_filter[0])) and (int(training.time) <= int(time_filter[1])):
                filtered.append(training)
        return filtered
            
