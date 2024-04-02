# import knihoven
from tkinter import *
import customtkinter as ctk
from datetime import date
from icecream import ic
# import souborů
from ctkWidgets import Frame, Label, Entry, Button, ComboBox
from configuration import colors, gender_label, gender, personal_data_path
from general import General


class PersonalDataFrame (Frame):
    """Načte frame s nastavením osobních údajů."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.personal_data = self._loadPersonalData()
        self._setLastPersValues()
        self.columnconfigure([0, 1, 2, 3], weight = 1)
        self._initGUI()
        self._updateButton()
        self._disabledForRestOfDay()

    def _initGUI(self) -> None:
        """Vytvoří grafucké rozhraní framu s nastavením osobních údajů."""
        # nadpis
        title_pad = 6
        title = Label(self, "Osobní údaje", ("Arial", 17))
        title.grid(row = 0, column = 0, sticky = ctk.W, columnspan = 4, padx = (15, title_pad), pady = title_pad)
        title.configure(text_color = colors["light"])
        # vstupy
        padx = 3
        pady = 2
        mass_label = Label(self, "Hmotnost (kg):")
        mass_label.grid(row = 1, column = 0, sticky = ctk.E, padx = padx)
        self.var_mass = StringVar()
        self.mass_entry = Entry(self, self.var_mass)
        self.mass_entry.grid(row = 1, column = 1, sticky = ctk.W, padx = padx, pady = pady)
        self.mass_entry.configure(width = 140)
        height_label = Label(self, "Výška (cm):")
        height_label.grid(row = 1, column = 2, sticky = ctk.E, padx = padx)
        self.var_height = StringVar()
        self.height_entry = Entry(self, self.var_height)
        self.height_entry.grid(row = 1, column = 3, sticky = ctk.W,padx = padx, pady = pady)
        self.height_entry.configure(width = 140)
        age_label = Label(self, "Věk:")
        age_label.grid(row = 2, column = 0, sticky = ctk.E, padx = padx)
        self.var_age = StringVar()
        self.age_entry = Entry(self, self.var_age)
        self.age_entry.grid(row = 2, column = 1, sticky = ctk.W,padx = padx, pady = pady)
        self.age_entry.configure(width = 140)
        gender_l = Label(self, "Pohlaví:")
        gender_l.grid(row = 2, column = 2, sticky = ctk.E, padx = padx)
        gender_var = StringVar()
        gender_cb = ComboBox(self, gender_label, self._changeOfGender, gender_var)
        gender_cb.grid(row = 2, column = 3, sticky = ctk.W, padx = padx, pady = pady)
        gender_cb.configure(width = 140)
        self.var_mass.set(self.mass)
        self.var_height.set(self.height)
        self.var_age.set(self.age)
        gender_cb.set(self.gender)

    def _updateButton (self) -> None:
        """Vytvoří tlačítko pro aktualizaci osobních údajů."""
        self.update_b = Button(self, "Aktualizovat", self._updatePersonalData)
        self.update_b.grid(row = 3, column = 0, columnspan = 4, sticky = ctk.E, padx = (10, 30), pady = 6)
        self.update_b.configure(height = 35, width = 110)

    def _loadPersonalData (self) -> dict:
        """Načte osobní údaje o uživateli z databáze osobních údajů. Vrátí slovník údajů zadaných v ruzných datech uživatelem."""
        file_lines = General.loadLinesFromFile(personal_data_path)
        for i in range(len(file_lines)):
            file_lines[i] = file_lines[i].split(":")
        personal_dict = { file_lines[0][0] : file_lines[0][1], }
        for i in range(1, len(file_lines)):
            if file_lines[i][0] in personal_dict.keys():
                personal_dict[file_lines[i][0]].append((file_lines[i][1], file_lines[i][2]))
            else:
                personal_dict[file_lines[i][0]] = [(file_lines[i][1], file_lines[i][2])]
        return personal_dict
    # odstran selfy
    
    def _setLastPersValues (self) -> None:
        """Nastaví poslední nastavené hodnoty osobních údajů o užovateli jako aktualní hodnoty."""
        self._setGender(self.personal_data["gender"][0])
        self.mass = self.personal_data["mass"][-1][0]
        self.height = self.personal_data["height"][-1][0]
        self.age = self.personal_data["age"][-1][0]

    def _updatePersonalData (self) -> None:
        """Uloží aktualizované osobní údaje do databáze."""
            # gender se nastavuje nezavisle na stiknutí tlačítka aktualizovat
        if self._checkEntries():
            today = date.today()
            lines = []
            lines.append(General.preparePersonalDBString("mass", self.var_mass.get(), today))
            lines.append(General.preparePersonalDBString("height", self.var_height.get(), today))
            lines.append(General.preparePersonalDBString("age", self.var_age.get(), today))
            General.appendToFile(personal_data_path, lines)
            self._disableUpdating()

    def _checkEntries (self) -> bool:
        """Zkontroluje uživatelské vstupy, pokud jsou platné, provede se uložení dat."""
        mass = self._checkOneEntry(self.mass_entry, self.var_mass.get())
        height = self._checkOneEntry(self.height_entry, self.var_height.get())
        age = self._checkOneEntry(self.age_entry, self.var_age.get())
        return mass and height and age
        
    def _checkOneEntry (self, entry_widget : object, entry_text : str) -> bool:
        """Zkontroluje, zda je proměnná správně zadána -> Ano - vrátí True, Ne - vrátí false a orámuje entry červeně."""
        if entry_text.isnumeric():
            General.setDefaultBorder(entry_widget)
            return True
        else:
            General.setRedBorder(entry_widget)
            return False

    def _changeOfGender (self, value) -> None:
        """Zkontroluje zda se zadání pohlaví změnilo, pokud ne, nic se nestane pokud ano, přepíše se v soubrou databáze osobních údajů."""
        index = gender_label.index(value)
        if gender[index] != self.personal_data["gender"][0]:
            self.personal_data['gender'] = gender[index]
            file_lines = General.loadLinesFromFile(personal_data_path)
            file_lines[0] = "{1}{0}{2}\n".format(':', 'gender', self.personal_data['gender'])
            General.overwriteFile(personal_data_path, file_lines)

    def _setGender (self, value : str) -> None:
        """Nastaví pohlaví uživatele a uloží do databáze."""
        for i in range(len(gender)):
            if value == gender_label[i] or value == gender[i]:
                self.gender = gender_label[i]

    def _disabledForRestOfDay (self) -> None:
        """Při inicializaci zkontroluje, zda je ještě možné dnes data změnit."""
        today = date.today()
        for key in self.personal_data:
            if key == "gender": continue
            for item in self.personal_data[key]:
                if General.stringToDate(item[1]) == today:
                    self._disableUpdating()

    def _disableUpdating (self) -> None:
        """Znemožní updatování osobních údajů nastavením stavu disabled pro entry a tlačítka."""
        self.mass_entry.configure(state = DISABLED)
        self.var_mass.set("")
        self.height_entry.configure(state = DISABLED)
        self.var_height.set("")
        self.age_entry.configure(state = DISABLED)
        self.var_age.set("")
        self.update_b.configure(state = DISABLED)