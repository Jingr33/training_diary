"""Soubor pro ukládání konfiguračních konstant."""

# list možných sportů pro zadání tréninku
sport_list = ["posilovna", "běh"]
# barvy jednotlivých sportů #TODO nastavovatelnost
sport_color = {
    sport_list[0] : "#e74c3c",
    sport_list[1] : "#3498db",
}

# list výběrových tlačítek v menuFramu
menu_list = ["Přehled", "Kalendář", "Další"]

# cesta k souboru se všemi uloženými tréninky
path = "training_database.txt"

# jednotlivé části těla pro treénink v posilovně
gym_body_parts = ["Nohy", "Střed těla", "Prsa", "Ramena", "Záda", "Biceps", "Triceps", "Předloktí"]

# legenda tabulky v přehledu tréninků
legend = ["Datum", "Sport", "Čas", "Detaily ->"]

# slovník měsíců v roce
months = {
    1 : "leden",
    2 : "únor",
    3 : "březen",
    4 : "duben",
    5 : "květen",
    6 : "červen",
    7 : "červenec",
    8 : "srpen",
    9 : "září",
    10 : "říjen",
    11 : "listopad",
    12 : "prosinec",
}