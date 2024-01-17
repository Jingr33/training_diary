#importy souborů
from configuration import sport_list, gym_body_parts

class OneTaining ():
    """Třída pro vytvoření instance jednoho tréninku z dat v souboru."""
    def unlockTheData(self, file_line):
        """Funkce rozklíčuje data ze souboru a přiřadí je objektu."""
        # rozdělení řádku ze souboru na jednolivé údaje
        data_list = self._separateData(file_line)

        # uložení data tréninku
        self.date = data_list[0]

        #rozdělení tréninku podle sportu
        self.sport = self._whichSport(data_list)

        # rozklíčuje a přiřadí data jako vlastnosti tréninku.
        self._findData(data_list)

        if self.sport == sport_list[0]:
            self.practicedParts = self._practicedPartsString()
            print(self.practicedParts)

    def _practicedPartsString (self):
        "Vytvoří string procvčených částí těla."
        # pole částí těla
        parts = [self.leg, self.core, self.breast, self.shoulders, self.back,
                 self.biceps, self.triceps, self.forearm]
        # vytvoření slovního podání odcvičených částí těla
        practiced_parts = ""
        text = ""
        i = 0
        for part in parts: # přes věechny možné odcvičené části těla
            if part == 1: # pokud byla odcvičena
                if practiced_parts != "": #udělá se mezery mezi slovy
                    text = ", "
                text = text + gym_body_parts[i]
                practiced_parts = practiced_parts + text
            i = i + 1
        return practiced_parts

    def _separateData(self, data_line):
        """Rozdělení dat z řádku na jednotlivé údaje."""
        data_list = data_line.split(" / ")
        del data_list[-1]
        return data_list

    def _whichSport (self, data_list):
        """Zjistí, o který sport se jedná."""
        if data_list[1] == sport_list[0]:
            sport = sport_list[0]
        elif data_list[1] == sport_list[1]:
            sport = sport_list[1]
        else:
            ... #TODO
        return sport
    
    def _findData(self, data_list):
        """Rozklíčuje data daného tréninku."""
        if self.sport == sport_list[0]:
            self._gymData(data_list)
        elif self.sport == sport_list[1]:
            self._runData(data_list)
        else:
            ... #TODO

    def _runData(self, data_list):
        """Rozklíčuje data běžeckého tréninku."""
        self.time = data_list[2]
        self.distance = data_list[3]

    def _gymData(self, data_list):
        self.time = int(data_list[2])
        self.leg = int(data_list[3])
        self.core = int(data_list[4])
        self.breast = int(data_list[5])
        self.shoulders = int(data_list[6])
        self.back = int(data_list[7])
        self.biceps = int(data_list[8])
        self.triceps = int(data_list[9])
        self.forearm = int(data_list[10])