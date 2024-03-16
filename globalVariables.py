"""NAČTENÍ NASTAVENÍ Z DATABÁZE UŽIVATELSKÉHO NASTAVENÍ APLIKACE"""
def loadSettingDatabase () -> dict:
    """Načte databázi nastavení aplikace do slovníku."""
    with open ("setting_database.txt", "r") as f:
        lines = f.readlines()
        global setting
    setting = {}
    for line in lines:
        key, value = line.split(":")
        setting[key] = value
    return setting

def overwriteSettingFile () -> None:
    """Přepíše databázi nastavení aplikace, uloží nově provedené změny."""
    file_lines = [None] * len(setting)
    i = 0
    for item in setting:
        one_line = item + ":" + str(setting[item])
        file_lines[i] = one_line
        i = i + 1
    with open ("setting_database.txt", "w") as f:
        f.writelines(file_lines)

def getAutoFullscreen () -> int:
    return int(setting["auto-fullscreen"])