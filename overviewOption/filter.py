# importy souborů
from configuration import sport_list, gym_body_parts

class Filter():
    """Filtruje tréninky podle vybraných parametrů."""
    def __init__(self, trainings, date_filter, sport_filter, time_filter, detail_filter):
        self.trainings = trainings

        # vyfiltrování podle filtrovaných sportů
        self.filtered_data = self._sportFiltrator(sport_filter)

        # vyfiltrování podle filtrovaného data
        self.filtered_data = self._dateFiltrator(date_filter)

        # vyfiltrování data podle času
        self.filtered_data = self._timeFiltrator(time_filter)

        # vyfiltrování podle detailů sportů
        self.filtered_data = self._detailsFiltrator(detail_filter)

    
    def getFilteredData(self):
        return self.filtered_data
    
    def _sportFiltrator(self, sport_filter) -> list:
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
            for sport_name in desired_sports:
                if training.sport == sport_name:
                    filtered.append(training)
        return filtered

    def _dateFiltrator(self, date_filter) -> list:
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
    
    def _timeFiltrator(self, time_filter) -> list:
        """Vyfiltruje data podle času."""
        # pokud není filtr nastavený -> trénink projde filtrem vždy
        bottom_condition = False # podmínka při nezadaném spodním filtru
        top_condition = False # podmínika při nezadaném horním filtru
        # spodní hranice filtru
        if time_filter[0] == "":
            bottom_condition = True
            time_filter[0] = "0"
        # horní hranice filtru
        if time_filter[1] == "":
            top_condition = True
            time_filter[1] = "0"

        # vytřídění dat podle zadaných mezí
        filtered = []
        for training in self.filtered_data:
            if (((int(training.time) >= int(time_filter[0])) or bottom_condition)
                and (((int(training.time) <= int(time_filter[1]))) or top_condition)):
                filtered.append(training)
        return filtered
    
    def _detailsFiltrator(self, detail_filter :list) -> list:
        """Vyfiltruje data podle detalních možností sportů."""
        # zavolání jednotlivých funkcí
        # detaily posilovny
        if detail_filter[0]:
            self.filtered_data = self._gymPartsFiltrator(detail_filter[0])
        # detaily běhu
        self.filtered_data = self._rundistanceFiltrator(detail_filter[1])

        return self.filtered_data

    def _gymPartsFiltrator(self, gym_parts_filter :list) -> list:
        """Vyfiltruje posilovnu podle odcvičených částí."""
        # vytvoření pole s názvy zvolených sportů ve filtru
        strings_to_find = []
        for i in range(len(gym_body_parts)):
            if gym_parts_filter[i] == 1:
                strings_to_find.append(gym_body_parts[i])

        # cyklus přes tréninky
        filtered = []
        for training in self.filtered_data:
            # výběr posilovacích tréninků
            if training.sport == sport_list[0].lower():
                # každé slovo ze strings_to_find se zkusí najít v odcvičených sportech tréninku
                for i in range(len(strings_to_find)):
                    found = training.practicedParts.find(strings_to_find[i])
                    if found >= 0:
                        filtered.append(training)
                        break
            else:
                # pokud se nejedná o posilovnu, přidá se vždy
                filtered.append(training)
        
        return filtered

    def _rundistanceFiltrator(self, distance_run_filter :list) -> list:
        """Vyfiltruje běh podle vzdálenosti."""
        # pokud není filtr nastavený -> trénink projde filtrem vždy
        bottom_condition = False # podmínka při nezadaném spodním filtru
        top_condition = False # podmínika při nezadaném horním filtru
        # spodní hranice filtru
        if distance_run_filter[0] == "":
            bottom_condition = True
            distance_run_filter[0] = "0"
        # horní hranice filtru
        if distance_run_filter[1] == "":
            top_condition = True
            distance_run_filter[1] = "0"

        # vytřídění dat podle zadaných mezí
        filtered = []
        for training in self.filtered_data:
            if training.sport == sport_list[1]:
                if (((int(training.distance) >= int(distance_run_filter[0])) or bottom_condition)
                    and ((int(training.distance) <= int(distance_run_filter[1])) or top_condition)):
                    filtered.append(training)
            else:
                filtered.append(training)
        return filtered

    

