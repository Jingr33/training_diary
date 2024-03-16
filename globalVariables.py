from icecream import ic
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
    global sport_colors
    sport_colors = getSportColors()
    return setting

def overwriteSettingFile () -> None:
    """Přepíše databázi nastavení aplikace, uloží nově provedené změny."""
    setting["sport-colors"] = prepareSportColorsToFile()
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
    return sport_colors
    
def prepareSportColorsToFile () -> str:
    """Vytvoří ze slovníku řádek pro zapsání do souboru. Vrátí string."""
    ic(sport_colors)
    string = ""
    for key in sport_colors:
        ic(key)
        string = "{0}{1}={2};".format(string, key, sport_colors[key])
    string = string.replace("běh", "beh")
    return string