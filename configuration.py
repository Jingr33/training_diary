"""Soubor pro ukládání konfiguračních konstant."""

# list možných sportů pro zadání tréninku
sport_list = ["posilovna", "běh"]
free_day = "volno"
# barvy jednotlivých sportů #TODO nastavovatelnost
sport_color = {
    sport_list[0] : "#e74c3c",
    sport_list[1] : "#3498db",
}
ghost_color = {
    sport_list[0]: "#e6c8c5",
    sport_list[1]: "#b6cfe0",
}

# list výběrových tlačítek v menuFramu
menu_list = ["Přehled", "Kalendář", "Další"]

# nezadaný vstup
unknown_text = "nezadano"
unknown_text_label = "––"

# cesta k souboru se všemi uloženými tréninky
trainings_path = "training_database.txt"
# cesta k souboru s tréninkovými plány
cycle_plans_path = "cycle_plan_database.txt"

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

# paleta barev
colors = {
    "gray" : "#333333",
    "dark-gray" : "#2c2c2c",
    "light-gray" : "#444444",
    "dark-red" : "#850101",
    "dark-red-hover" : "#823e3e",
    "dark-blue" : "#012f57",
}

#barvy stupňů třídění tréninků v přehledu
sorting_bg = {
    0 : "transparent",
    1 : "#ffe200",
    2 : "#fce842",
    3 : "#f7ea83",
    4 : "#faf2b4",
}
sorting_text_color = {
    0 : "#ffffff",
    1 : "#000000",
    2 : "#000000",
    3 : "#000000",
    4 : "#000000",
}

# Overview - počet viditelných řádků na jedno zobrazení
displayed_rows = 20