#importy souborů
from sports.sport import Sport
from configuration import sport_list, sport_color

class Gym (Sport):
    """Třída pro funkce, které jsou specifické pro trénink typu posilovna."""
    def __init__(self):
        super().__init__()
        self.name = sport_list[0]
        self.color = sport_color[self.name]

    def createAttributes(self, training : object) -> list:
        self.message_attributes = ["datum", "sport", "čas", "cviky"]
        return self.message_attributes

    def createValues(self, training : object) -> list:
        """Metoda vytvoří list  atributů pro vepsání do tooltip message."""
        str_time  = str(training.time) + " min"
        self.message_values = [training.date, training.sport, str_time, training.practicedParts]
        return self.message_values
