# inport knihoven
from tkinter import *
import customtkinter as ctk
# import souborů
from overviewOption.updateTraining.updateWindow import UpdateWindow
from sports.setSport import SetSport
from ctkWidgets import Label, Button
from image import Image as img
from configuration import colors, trainings_path


class OneRow (ctk.CTkFrame):
    """Třída vytvoří jeden řádek tréninku v tabulce v přehledu tréninků."""
    def __init__(self, master: ctk.CTkBaseClass, one_training):
        super().__init__(master)
        self.training = one_training
        # listy jednotlivých typů widget
        self.content_wigets = []
        self.setting_widgets = []

        self._initGUI() # obsah tréninku
        self._initSettingButton() # button nastavení

    def _initGUI(self):
        """Metoda pro vytvření obsahu jednoho řádku v tabulce s daty o tréninku."""
        # label s datem tréninku
        date_l = Label(self, self.training.date)
        date_l.pack(side = LEFT, fill = ctk.Y)
        date_l.configure(width = 100, height = 40)
        self.content_wigets.append(date_l)

        sport_l = Label(self, self.training.sport)
        sport_l.pack(side = LEFT, fill = ctk.Y)
        sport_l.configure(width = 110, height = 40, anchor = ctk.W)
        self.content_wigets.append(sport_l)

        time_text = str(self.training.time) + " min"
        time_l = Label(self, time_text)
        time_l.pack(side = LEFT, fill = ctk.Y)
        time_l.configure(width = 70, height = 40, anchor = ctk.W)
        self.content_wigets.append(time_l)

        # vytvoření labelů s detailními informace o daných trénincách lišících se sportovní náplní tréninku
        SetSport.detailsInOverview(self)

    def _initSetting (self) -> None:
        """Vygeneruje widety ve variantě pro nastavení."""
        delete_button = Button(self, "Smazat", self._deleteRow)
        delete_button.pack(side = LEFT, fill = ctk.BOTH, expand=TRUE, padx = 4, pady = 4)
        delete_button.configure(fg_color = colors["dark-red"], hover_color = colors["dark-red-hover"])
        self.setting_widgets.append(delete_button)

        update_button = Button(self, "Upravit", self._updateRow)
        update_button.pack(side = LEFT, fill = ctk.BOTH, expand = TRUE, padx = 4, pady = 4)
        update_button.configure(fg_color = colors["dark-blue"])
        self.setting_widgets.append(update_button)

    def _initSettingButton (self) -> None:
        """Vytvoří button s nastavením pro úpravu nebo smazání tréninku."""
        # udává, zda je řádek právě v nastavení pro zobrazení tréninku nebo zobrazení nastavení
        self.is_setting = False
        # vytvoření obrázku
        image = img("images\setting_icon.JPG", (20, 20))
        # button
        self.setting_button = Button(self, "", self.rowSettings)
        self.setting_button.pack(side=RIGHT, fill = ctk.Y, pady = 5, padx = 5)
        self.setting_button.configure(width = 25, height = 30, image = image)

    def rowSettings (self) -> None:
        """Funkce přegeneruje řádek tréninku na možnosti úprav při kliknutí na tlačítko nastavení."""
        #zavolání vygenerování nastavení nebo zpětného vygenerování obsahu tréninku
        if self.is_setting:
            self._trainingWidgets() # zpětné vypsání údajů tréninku
        else:
            self._settingWidgets() # vygenerování nastavení
        # nastavení proměnné is_setting
        self._contentSwitcher() 

    def _contentSwitcher (self) -> None:
        """Funkce přepíná proměnnou self.is_setting -> udává, zda je řádek v režimu 
        zobrazení tréninku, nebo v režimu zobrazení nastavení."""
        if self.is_setting:
            self.is_setting = False
        else:
            self.is_setting = True

    def _settingWidgets (self) -> None:
        """Přegeneruje řádek na nastavení."""
        # vymazání předchozích widget
        self._destroyOldWidgets(self.content_wigets)
        # změna obrázku v setting_buttonu
        self._changeButtonImage()
        # zobrazení widget nastavení
        self._initSetting()

    def _trainingWidgets (self) -> None:
        """Přegeneruje řádek zpět na variantu s obsahem tréninku."""
        # vymazání předchozích widget
        self._destroyOldWidgets(self.setting_widgets)
        # změna obrázku v setting_buttonu
        self._changeButtonImage()
        # zobrazení obsahu tréninku
        self._initGUI()

    def _destroyOldWidgets (self, widgets : list) -> None:
        """Metoda vymaže widgety starého framu (uvolní místo pro nový)."""
        for widget in widgets:
            widget.pack_forget()

    def _changeButtonImage (self) -> None:
        """Změní obrázek v setting_buttonu."""
        if self.is_setting:
            image = img("images//setting_icon.JPG", (20, 20))
        else:
            image = img("images//back_icon.png", (20, 20))
        self.setting_button.configure(image = image)

    def _deleteRow(self) -> None:
        """Metoda smaže řádek z tabulky a vymaže trénink ze záznamů po kliknutí na 
        tlačítko smazat."""
        # vymazání tréninku z databázového souboru s tréninky
        self._deleteFromFile(trainings_path, self.training.id)
        # zničení framu s řádkem tréninku
        self._frameDestroy()

    def _updateRow(self) -> None:
        """Metoda umožní upravit záznamy o tréninku po kliknutí na tlačítko upravit."""
        UpdateWindow(self, self.training) # otevření okna s úpravami

    def _deleteFromFile (self, path : str, training_id : int) -> None:
        """Vymaže trénink z databáze tréninků."""
        with open(path, "r+") as f:
            rows = f.readlines() # načtení souboru po řádcích
            f.seek(0) # kurzor na začátek
            for i in range(len(rows)):
                if (i + 1) != training_id:
                    f.write(rows[i])

    def _frameDestroy (self) -> None:
        """Smazaní řádku s térninkem z tabulky v Overview."""
        self.destroy()