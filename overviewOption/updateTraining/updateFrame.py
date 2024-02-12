#importy knihoven
from tkinter import *
import customtkinter as ctk
# impor souborů
from oneTraining import OneTraining
from sports.setSport import SetSport
from ctkWidgets import Frame, Label, Entry, ComboBox, Button
from configuration import sport_list
from general import General


class UpdateFrame (Frame):
    """Frame obsahující nastavení tréninku v updatovacím okně tréninku.."""
    def __init__ (self, master : ctk.CTkBaseClass, training : object):
        super().__init__(master)
        self.master = master
        self.training = training
        self.configure(corner_radius = 0)
        self.next_row = 0
        self.box_width = 120
        self.label_padx = 5
        self.specific_widgets = []
        self._initGUI() # widgety

    def _initGUI(self) -> None:
        """Grafické rozhraní úprav tréninku."""
        self.columnconfigure([0, 1, 2, 3], weight=1)
        self.rowconfigure([0,1,2,3,4,5,6], weight=1)
        self._mainGUI()
        self._specificGUI(self.training.sport)
        self._saveButton()
        
    def _mainGUI(self) -> None:
        """Widgety, které jsou pro každý trénink stejné."""
        date_l = Label(self, "Datum:")
        date_l.grid(column = 0, row=self.next_row, sticky = ctk.E, padx=self.label_padx)

        self.var_date = StringVar()
        date_e = Entry(self, self.var_date)
        date_e.grid(column = 1, row=self.next_row)
        date_e.configure(width = self.box_width)
        self.var_date.set(self.training.date)

        sport_l = Label(self, "Sport:")
        sport_l.grid(column = 2, row = self.next_row, sticky = ctk.E, padx=self.label_padx)

        self.sport_cb = ComboBox(self, sport_list, self._regenerateSpecificGUI, self.training.sport)
        self.sport_cb.grid(column = 3, row=self.next_row)
        self.sport_cb.configure(width = self.box_width)
        self.sport_cb.set(self.training.sport)

        time_l = Label(self, "Čas:")
        time_l.grid(column = 0, row = self.next_row + 1, sticky=ctk.E, padx=self.label_padx)

        self.var_time = StringVar()
        time_e = Entry(self, self.var_time)
        time_e.grid(column = 1, row=self.next_row + 1)
        time_e.configure(width = self.box_width)
        self.var_time.set(self.training.time)

        self.next_row = 2 # následující řádek

    def _specificGUI (self, value : str) -> None:
        """Widgety specifické pro každý typ sportu."""
        SetSport.updateTrainingGUI(self, self.training, value)

    def _saveButton (self) -> None:
        """Ukládací tlačítko."""
        self.save_button = Button(self, "Upravit", self._updateTraining)
        self.save_button.grid(column = 2, columnspan = 2, row = self.next_row)
        self.specific_widgets.append(self.save_button)

    def _regenerateSpecificGUI (self, value) -> None:
        """Přegeneruje widgegty ve framu při přepnutí sportu v comboboxu."""
        if self.specific_widgets:
            self.specific_widgets = General.deleteListWidgets(self.specific_widgets)
        self.next_row = 2 # upravení následujícího řádku
        self._specificGUI(value)
        self._saveButton()

    def _updateTraining (self) -> None:
        """uloží změny v tréninku do databáze tréninků."""
        values = self._getValuesList()
        OneTraining(self, operation="update", data_list = values) # vytvoření tréninku s novými údaji
        self.master.kill()
        self.master.master.deleteRow() # smazání starého tréninku

    def _getValuesList (self) -> list:
        """Vrátí list zadaných hodnot."""
        self.main_values = [self.var_date.get(), self.sport_cb.get(), self.var_time.get()]
        SetSport.updateTrainingData(self)
        return self.main_values
    