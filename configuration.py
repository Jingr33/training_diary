"""Soubor pro ukládání konfiguračních konstant."""

# list možných sportů pro zadání tréninku
sport_list = ["posilovna", "běh"]
free_day = "volno"
# barvy jednotlivých sportů #TODO nastavovatelnost
sport_color = {
    sport_list[0] : "#3498DB", # posilovna
    sport_list[1] : "#C0392B", # běh
}
# ghost_color = {
#     sport_list[0]: "#3498DB",
#     sport_list[1]: "#C0392B",
# }

# list výběrových tlačítek v menuFramu
menu_list = ["Přehled", "Kalendář", "Statistiky"]

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
    "dark-gray-2" : "#262626",
    "light-gray" : "#444444",
    "dark-red" : "#850101",
    "dark-red-hover" : "#823e3e",
    "dark-blue" : "#012f57",
    "light-blue" : "#98d9ed",
    "black" : "#000000",
}

# barevná paletta pro koláčový graf 
pie_chart_palette = {
    "Nohy" : "#009596",
    "Střed těla" : "#003737",
    "Prsa" : "#F4C145",
    "Ramena" : "#C58C00",
    "Záda" : "#F0AB00",
    "Biceps" : "#EF9234",
    "Triceps" : "#EC7A08",
    "Předloktí" : "#C46100",
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

# možnosti v nastavení období, pro které graf vyobrazuje hodnoty 
chart_range_option = ["den", "týden", "měsíc", "rok"]

# pozadí framů s grafem
chart_frame_color = "#262626"

# stringy grafu podrobností posilovny
gym_chart_strings = {
    "title" : "Poměr odcvičených částí těla",
}
# stringy grafu podrobností běhu
run_chart_strings = {
    ...
}