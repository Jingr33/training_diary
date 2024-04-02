from icecream import ic
# import souborů
from configuration import all_sports


"""NAČTENÍ NASTAVENÍ Z DATABÁZE UŽIVATELSKÉHO NASTAVENÍ APLIKACE"""
def loadSettingDatabase () -> dict:
    """Načte databázi nastavení aplikace do slovníku."""
    with open ("setting_database.txt", "r") as f:
        lines = f.readlines()
    global setting
    setting = {}
    for line in lines:
        line = line.strip()
        key, value = line.split(":")
        setting[key] = value
    global selected_sports
    selected_sports = getSelectedSports()
    global sport_list
    sport_list = getSportList(selected_sports)
    global sport_color
    sport_color = getSportColors()
    ic(sport_color)
    return setting

def overwriteSettingFile () -> None:
    """Přepíše databázi nastavení aplikace, uloží nově provedené změny."""
    setting["sport-colors"] = prepareSportColorsToFile()
    setting["selected-sports"] = prepareSelectedSportsToFile()
    file_lines = [None] * len(setting)
    i = 0
    for item in setting:
        one_line = item + ":" + str(setting[item]) + "\n"
        file_lines[i] = one_line
        i = i + 1
    with open ("setting_database.txt", "w") as f:
        f.writelines(file_lines)

def getAutoFullscreen () -> int:
    return int(setting["auto-fullscreen"])

def getSportColors () -> dict:
    """Vrátí slovník, kde klíč je název sportu a hodnota jeho barva."""
    sport_colors = {}
    sports = setting["sport-colors"].split(";")
    del sports[-1]
    for sport in sports:
        key, value = sport.split("=")
        sport_colors[key] = value
    sport_colors["běh"] = sport_colors["beh"]
    del sport_colors["beh"]
    sport_colors["plavání"] = sport_colors["plavani"]
    del sport_colors["plavani"]
    return sport_colors

def getSelectedSports () -> list:
    """Vrátí list hodnot 1 / 0, které udávájí, zda se daný sport mám zorbazovat v aplikaci nebo ne."""
    selected_list = setting["selected-sports"].split(";") # rozdělení na hodnoty
    del selected_list[-1] # vymazání poslední přebývající hodnoty
    for i in range(len(selected_list)): # převedení na int
        selected_list[i] = int(selected_list[i])
    return selected_list

def getSportList (selected_sport : list) -> list:
    """Vrátí list s názvy (string) sportů, které jsou aktivivány k využívaní. Vstup je list 1 / 0 hodnot ke každému sportu."""
    sport_list = []
    for i in range(len(all_sports)):
        if selected_sport[i]:
            sport_list.append(all_sports[i])
    return sport_list
    
def prepareSportColorsToFile () -> str:
    """Vytvoří ze slovníku řádek pro zapsání do souboru. Vrátí string."""
    string = ""
    for key in sport_color:
        string = "{0}{1}={2};".format(string, key, sport_color[key])
    string = string.replace("běh", "beh")
    string = string.replace("plavání", "plavani")
    return string

def prepareSelectedSportsToFile () -> str:
    """Vytvoří string z listu selected_sports pro zapsání zpět do souboru., Vrátí string."""
    string = ""
    for item in selected_sports:
        string = "{0}{1};".format(string, str(item))
    return string