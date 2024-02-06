#import knihoven
from datetime import date
from time import *
#importy souborů

class Sorting ():
    """Obsahuje funkce pro třídění tréninků v přehledu všech tréninků."""
    def __init__(self, trainings : list, sort_levels : dict):
        self.trainings = [trainings] # vytvoří se 2D list
        self.sort_levels = sort_levels # slovník úrovní jedlotlivých položek k setřídění
        # slovník přiřazující třídící metodu k jednotlivým tlačítkům
        self.sort_functions = {
            "b_date" : self._sortByDate,
            "b_sport" : self._sortBySport,
            "b_time" : self._sortByTime,
            "b_details" : self._sortByDetails,
        }

        # střídění tréninků
        self._sortInOrder()

    def GetSortedTrainings (self) -> list:
        """Vrátí list setříděných tréninků."""
        self.sorted_trainings = self._toOneList(self.sorted_trainings)
        return self.sorted_trainings
    
    def _toOneList(self, group_trains : list) -> None:
        """Vícerozměrné listy přehází do jednorozměrného pole za sebe."""
        # pokud se déka listu původních a stříděných tréninků nerovná, znamená to,
        # že ještě obsahuje nějaký vnitřní list
        while len(group_trains) != len(self.trainings[0]):
            one_dimension = [] #jednorozměrný list
            for item in group_trains:
                one_dimension = one_dimension + item
            group_trains = one_dimension
        return group_trains

    def _sortInOrder (self) -> None:
        """Vytvoří pořadí třídících funkcí, v kterém se mají postupně volat a zavolá je."""
        # setřídění slovníku s úrovněmi podle úrovní a vrátí list
        sorting_order = self._makeSortOrder()
        # zavolání třídících funkcí v pořadí
        self._sortData(sorting_order)
    
    def _makeSortOrder (self) -> list:
        """Setřídí položky podle úrovní."""
        sort_tuples = sorted(self.sort_levels.items(), key=lambda x: x[1])
        # přidání klíču slovníku úrovní do listuv pořadí třídění
        sorting_list = []
        for elem in sort_tuples:
            if elem[1] == 0: # vyřazení nulových úrovní
                del elem
            else:
                sorting_list.append(elem[0])
        return sorting_list

    def _sortData (self, sorting_order : list) -> None:
        """Zavolání třídících funkcí v daném pořadí."""
        to_sort = self.trainings # data k setřídění
        # postupné zavolání třídících funkcí
        for index in sorting_order:
            if self.sort_levels[index] > 0: # aby se prvky s úrovní 0 netřídily
                to_sort = self.sort_functions[index](to_sort)
        self.sorted_trainings = to_sort

    def _sortByDate (self, to_sort : list) -> list:
        """Setřídí vložené listy v listu (2D listy) podle datumu a vrátí ho."""
        #střídění zvlášť pro každou třídící podskupinu (vnitřnější list v 2d list)
        for group in to_sort:
            ...
        return to_sort

    def _sortBySport (self, to_sort : list) -> list:
        """Setřídí vložené listy v listu (2D listy) podle sportu a vrátí ho."""
        sorted = []
        for group in to_sort:
            # list indexů pro slovníky
            index_list = self._indexList(len(group))
            # slovník tréninků
            trainings = self._trainingDict(group, index_list)
            # slovník sport pro třídění
            sort_elems = self._sortSportDict(group, index_list)
            # roztříděný list tréninků
            sorted = self._sortIt(sort_elems, trainings)
        #rozdělení do listů pro další třídění
        to_sort = self._ungroupSport(sorted)
        return to_sort

    def _sortByTime (self, to_sort : list) -> list:
        """Setřídí vložené listy v listu (2D listy) podle času a vrátí ho."""
        sorted = []
        for group in to_sort:
            # list indexů pro slovníky
            index_list = self._indexList(len(group))
            # slovník tréninků
            trainings = self._trainingDict(group, index_list)
            # slovník časů pro třídění
            sort_elems = self._sortTimeDict(group, index_list)
            # roztříděný list tréninků
            sorted = self._sortIt(sort_elems, trainings)
        #rozdělení do listů pro další třídění
        to_sort = self._ungroupTime(sorted)
        return to_sort

    def _sortByDetails (self, to_sort : list) -> list:
        """Setřídí vložené listy v listu (2D listy) podle detailů a vrátí ho."""
        for group in to_sort:
            ...
        return to_sort
    
    def _indexList(self, lenght : int) -> list:
        """Vrátí list indexů o velikosti jedné skupiny tréninků."""
        return list(range(lenght))
    
    def _trainingDict (self, group : object, index_list : list) -> dict:
        """Vrátí slovník s tréninky a jejich klíči."""
        trainings = {}
        for i in range(len(group)):
            trainings[index_list[i]] = group[i]
        return trainings

    def _sortSportDict (self, group : object, index_list : list) -> dict:
        """Vrátí slovník s prvky podle kterých se třídí a jejich klíči."""
        sort_elems = {}
        for i in range(len(group)):
            sort_elems[index_list[i]] = group[i].sport
        return sort_elems
    
    def _sortTimeDict (self, group : object, index_list : list) -> dict:
        """Vrátí slovník s prvky podle kterých se třídí a jejich klíči."""
        sort_elems = {}
        for i in range(len(group)):
            sort_elems[index_list[i]] = int(group[i].time)
        return sort_elems

    def _sortIt (self, sort_elems : dict, trainings : dict) -> list:
        """Setřídí prvky ve slovníku podle kterého se třídí, 
        uspořádá slovník s tréniky a vrátí ho."""
        # uspořadání třídícího slovníku
        sort_elems = sorted(sort_elems.items(), key=lambda x: x[1])
        # vytvoření listu s uspořádanými tréninky
        sorted_trainings = [None] * len(trainings)
        i = 0
        for elem in sort_elems:
            sorted_trainings[i] = trainings[elem[0]]
            i = i + 1
        return sorted_trainings
    
    def _ungroupSport (self, sort_dict : dict) -> list:
        """Rozdělí list do listů pro další úrovně třídění."""
        groups = {}
        # cyklus přes tréninky v uspořadaném slovníku tréninků
        for training in sort_dict:
            if training.sport in groups.keys(): # pokud už list s klíčovým slovem existuje
                groups[training.sport].append(training)
            else: # pokud list s klíčovým slovem neexistuje, vytvoří se nový
                groups[training.sport] = [training]
        # spojení jednotlivých skupin do jednoho nadlistu
        for_sort = self._createOverlist(groups)
        return for_sort
    
    def _ungroupTime (self, sort_dict : dict) -> list:
        """Rozdělí list do listů pro další úrovně třídění."""
        groups = {}
        # cyklus přes tréninky v uspořadaném slovníku tréninků
        for training in sort_dict:
            if training.time in groups.keys():# pokud už list s klíčovým slovem existuje
                groups[training.time].append(training)
            else: # pokud list s klíčovým slovem neexistuje, vytvoří se nový
                groups[training.time] = [training]
        # spojení jednotlivých skupin do jednoho nadlistu
        for_sort = self._createOverlist(groups)
        return for_sort
    
    def _createOverlist (self, groups : dict) -> list:
        """Vytvoří nadlist složený z vnitřích listů jednotlivých skupin."""
        for_next_sort = []
        for group in groups:
            for_next_sort.append(groups[group])
        return for_next_sort
