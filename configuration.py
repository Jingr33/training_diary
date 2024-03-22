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
menu_list = ["Přehled", "Kalendář", "Statistiky", "Možnosti"]

# nezadaný vstup
unknown_text = "nezadano"
unknown_text_label = "––"

# cesta k souboru se všemi uloženými tréninky
trainings_path = "training_database.txt"
# cesta k souboru s cyklickými tréninkovými plány
cycle_plans_path = "cycle_plan_database.txt"
# cesta k souboru s jednoduchými tréninkovými plány
single_plans_path = "single_plan_database.txt"

# jednotlivé části těla pro treénink v posilovně
gym_body_parts = ["Nohy", "Střed těla", "Prsa", "Ramena", "Záda", "Biceps", "Triceps", "Předloktí"]

# legenda tabulky v přehledu tréninků
legend = ["Datum", "Sport", "Čas", "Detaily ->"]

# slovník měsíců v roce
months = {
    1 : "Leden",
    2 : "Únor",
    3 : "Březen",
    4 : "Duben",
    5 : "Květen",
    6 : "Červen",
    7 : "Červenec",
    8 : "Srpen",
    9 : "Září",
    10 : "Říjen",
    11 : "Listopad",
    12 : "Prosinec",
}

# dny v týdnu
days_in_week = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]

# paleta barev
colors = {
    "gray" : "#333333",
    "dark-gray" : "#2c2c2c",
    "dark-gray-2" : "#262626",
    "dark-gray-3" : "#282828",
    "light-gray" : "#444444",
    "dark-red" : "#850101",
    "dark-red-hover" : "#823e3e",
    "dark-blue" : "#012f57",
    "light-blue" : "#98d9ed",
    "free-day-gray" : "#2f2f2f",
    "black" : "#000000",
    "entry-border" : "#5a5a5a",
    "light" : "#c7c7c7",
    "dodger-blue-3" : "#1874CD",
    "dodger-blue-2" : "#1E90FF",
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
    "title" : "Celkové uběhnutá vzdálenost"
}