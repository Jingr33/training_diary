#import knihoven
from datetime import date
from time import *
#importy souborů
from sports.setSport import SetSport

class Sorting ():
    """Obsahuje funkce pro třídění tréninků v přehledu všech tréninků."""
    def __init__(self, trainings : list, sort_levels : dict):
        self.trainings = trainings # vytvoří se 2D list
        self.sort_levels = sort_levels # slovník úrovní jedlotlivých položek k setřídění
        self.unsortable = [] # pro tréninky, které nelze setřídit
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
        self.sorted_trainings.extend(self.unsortable)
        return self.sorted_trainings
    
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
        sorting_order.reverse()
        # postupné zavolání třídících funkcí
        for index in sorting_order:
            if self.sort_levels[index] > 0: # aby se prvky s úrovní 0 netřídily
                to_sort = self.sort_functions[index](to_sort)
        self.sorted_trainings = to_sort

    def _sortByDate (self, to_sort : list) -> list:
        """Setřídí vložené listy v listu (2D listy) podle datumu a vrátí ho."""
        #střídění zvlášť pro každou třídící podskupinu (vnitřnější list v 2d list)
        sorted = []
        # list indexů pro slovníky
        index_list = self._indexList(len(to_sort))
        # slovník tréninků
        trainings = self._trainingDict(to_sort, index_list)
        # slovník sport pro třídění
        sort_elems = self._sortDateDict(to_sort, index_list)
        # roztříděný list tréninků
        to_sort = self._sortIt(sort_elems, trainings)
        return to_sort

    def _sortBySport (self, to_sort : list) -> list:
        """Setřídí vložené listy v listu (2D listy) podle sportu a vrátí ho."""
        sorted = []
        # list indexů pro slovníky
        index_list = self._indexList(len(to_sort))
        # slovník tréninků
        trainings = self._trainingDict(to_sort, index_list)
        # slovník sport pro třídění
        sort_elems = self._sortSportDict(to_sort, index_list)
        # roztříděný list tréninků
        to_sort = self._sortIt(sort_elems, trainings)
        return to_sort

    def _sortByTime (self, to_sort : list) -> list:
        """Setřídí vložené listy v listu (2D listy) podle času a vrátí ho."""
        sorted = []
        # vyřazení tréninků, které není možné setřídit
        to_sort = self._elimUnsortable(to_sort, "time") 
        # list indexů pro slovníky
        index_list = self._indexList(len(to_sort))
        # slovník tréninků
        trainings = self._trainingDict(to_sort, index_list)
        # slovník časů pro třídění
        sort_elems = self._sortTimeDict(to_sort, index_list)
        # roztříděný list tréninků
        to_sort = self._sortIt(sort_elems, trainings)
        return to_sort

    def _sortByDetails (self, to_sort : list) -> list:
        """Setřídí vložené listy v listu (2D listy) podle detailů a vrátí ho."""
        sorted = []
        # vyřazení tréninků, které není možné setřídit
        to_sort = self._elimUnsortable(to_sort, "distance") 
        # list indexů pro slovníky
        index_list = self._indexList(len(to_sort))
        # slovník tréninků
        trainings = self._trainingDict(to_sort, index_list)
        # roztříděný list tréninků
        to_sort = self._sortIt_details(trainings)
        return to_sort
    
    def _indexList(self, lenght : int) -> list:
        """Vrátí list indexů o velikosti jedné skupiny tréninků."""
        return list(range(lenght))
    
    def _trainingDict (self, to_sort : object, index_list : list) -> dict:
        """Vrátí slovník s tréninky a jejich klíči."""
        trainings = {}
        for i in range(len(to_sort)):
            trainings[index_list[i]] = to_sort[i]
        return trainings
    
    def _sortDateDict (self, to_sort : object, index_list : list) -> dict:
        """Vrátí slovník s prvky datumů (podle kterých se třídí) a jejich klíče."""
        sort_elems = {}
        for i in range(len(to_sort)):
            str_date = to_sort[i].date
            date_list = str_date.split(". ")
            day = date(2000 + int(date_list[2]), int(date_list[1]), int(date_list[0]))
            sort_elems[index_list[i]] = day
        return sort_elems
    
    def _sortSportDict (self, to_sort : object, index_list : list) -> dict:
        """Vrátí slovník se sporty (podle kterých) se třídí a jejich klíči."""
        sort_elems = {}
        for i in range(len(to_sort)):
            sort_elems[index_list[i]] = to_sort[i].sport
        return sort_elems
    
    def _sortTimeDict (self, to_sort : object, index_list : list) -> dict:
        """Vrátí slovník s časy (podle kterých se třídí) a jejich klíči."""
        sort_elems = {}
        for i in range(len(to_sort)):
            sort_elems[index_list[i]] = int(to_sort[i].time)
        return sort_elems
    
    def _sortDistanceDict (self, to_sort : object, index_list : list) -> dict:
        """Vrátí slovník s časy (podle kterých se třídí) a jejich klíči."""
        sort_elems = {}
        for i in range(len(to_sort)):
            sort_elems[index_list[i]] = float(to_sort[i].distance)
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
    
    def _sortIt_details (self, trainings : dict) -> list:
        """Setřídí prvky ve slovníku podle kterého se třídí, 
        uspořádá slovník s tréniky a vrátí ho. Ale dělá to jen pro třídění detailů 
        jednotlivých sportů."""
        # rozřazení do skupin podle jednotlivých sportů
        sports = {}
        for training in trainings:
            if trainings[training].sport in sports.keys(): # pokud už klíč existuje, trénink se přiřadí do pole
                sports[trainings[training].sport].append(trainings[training])
            else: # pokud ještě neexisuje, vytvoří se nový klíč a sním pole s tréninkem
                sports[trainings[training].sport] = [trainings[training]]
        # setřídí jednotlivé pole sportů
        for key in sports:
           sports[key] = self._sortEachDict(sports, key)
        # spojit listy zaye do jednoho
        sorted_trainings = []
        for key in sports:
            sorted_trainings = sorted_trainings + sports[key] 
        return sorted_trainings
    
    def _sortEachDict (self, training_dict : dict, key : str) -> list:
        """Vyhodnotí, zda se jednolivé listy třídí a setřídí je."""
        sorted_trainings = SetSport.sortEachTrainingDict(self, training_dict, key)
        return sorted_trainings
    
    def _elimUnsortable(self, trainings : list, criterion : str) -> list:
        """Vyřadí z tréninkového listu určeného k setřídění tréniky, které nelze
        uspořadát podle požadovaného kritéria. Vyřazené přidá do listu netříditelných tréninků."""
        checked_trainings = []
        for training in trainings:
            try:
                float(getattr(training, criterion))
                checked_trainings.append(training)
            except:
                self.unsortable.append(training)
        return checked_trainings
       
    def _createOverlist (self, groups : dict) -> list:
        """Vytvoří nadlist složený z vnitřích listů jednotlivých skupin."""
        for_next_sort = []
        for group in groups:
            for_next_sort.append(groups[group])
        return for_next_sort
