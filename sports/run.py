#importy souborů
from sports.sport import Sport
from configuration import sport_list, sport_color

class Run (Sport):
    """Třída pro funkce, které jsou specifické pro trénink typu běh."""
    def __init__(self):
        super().__init__()
        self.name = sport_list[1]
        self.color = sport_color[self.name]

    def createAttributes(self, training : object) -> list:
        """List názvů atributů tréninku vypisujících se do tooltipů."""
        self.message_attributes = ["datum", "sport", "čas", "vzdálenost"]
        return self.message_attributes

    def createValues(self, training : object) -> list:
        """Metoda vytvoří list  atributů pro vepsání do tooltip message."""
        str_time = str(training.time) + " min"
        str_distance = str(training.distance) + " km"
        self.message_values = [training.date, training.sport, str_time, str_distance]
        return self.message_values

        