# import knihoven
from tkinter import *
import customtkinter as ctk
from CTkToolTip import *
# import souborů
from oneTraining import OneTraining
from sports.setSport import SetSport
from ctkWidgets import Label
from configuration import sport_color

class OneActivity (Label):
    """Uchovává informace o aktivitách v jednotlivých dnech a vytváří pruh v náhledovém
    kalendáři (v nastavení cyklického tréninkového plánu)."""
    def __init__ (self, master : ctk.CTkBaseClass, selected_sport : str, details : tuple):
        self.font = ("Arial", 13)
        super().__init__(master, selected_sport, self.font)
        self.sport = selected_sport
        self.fg_color = sport_color[self.sport]
        self.tooltip_alpha = 0.9

        #vytvoření objektu tréninku ze zadaných údajů
        self.one_training = OneTraining()
        self.one_training.setPlanData(selected_sport, details)

        # barva pozadí
        self.configure(fg_color = self.fg_color, corner_radius = 5)


        #vytvoření textu zobrazujícího se v tooltipu
        self.message = SetSport().createTooltipMessage(self.one_training)
        # vytvoření tooltipu na stripem
        self.tooltip = CTkToolTip(self, delay=0.2, message = self.message, justify = 'left', 
                   alpha = self.tooltip_alpha, x_offset= -50, y_offset=-100)
        
        # animační proměnné
        self.destroy_time = 300

        # eventy pro mazání aktivit
        self.bind("<Button-1>", self._destroyOption)

        #TODO nakonec se při uložení sem musí uložit taky pořadí dne, v tréninkovém plánu

    def bindWithDay(self, day_number : int) -> None:
        """Metoda přidá do listu s daty o tréniku pořadí dne, ve kterém je."""
        self.data[0] = day_number

    def _destroyOption(self, value) -> None:
        """Přemění strip na možnost vymazat ho (trénink) ze dne."""
        # skrytí tooltipu
        self.tooltip.hide()
        # přeměnění textu v labelu
        label_text = "SMAZAT " + self.sport.upper() + "\npravé tlačítko"
        self.configure(text = label_text, font = ("Arial", 10, "bold"),
                              fg_color = "red")
        # vytvoření nových eventů pro potvrzení či vrácení do původního stavu
        self.unbind("<Button-1>")
        self.bind("<Button-1>", self._activityRestoration)
        self.bind("<Button-3>", self._destroyActivity)

    def _activityRestoration (self, value) -> None:
        """Obnoví aktivitu, pokud se uživatel rozhodne ji nezrušit."""
        # znovuzobrazení tooltipu
        self.tooltip.show()
        # přepsání textu v labelu
        label_text = self.sport
        self.configure(text = label_text, font = self.font, fg_color = self.fg_color)
        # navrácení eventů do původního stavu pro aktivitu
        self.unbind("<Button-1>")
        self.unbind("<Button-3>")
        self.bind("<Button-1>", self._destroyOption)

    def _destroyActivity (self, value) -> None:
        """Vymaže aktivitu ze dne v náhledovém kalendáři."""
        # zprůhledňování aktivity a smazání aktivity
        self._detsroyAnimation()

    def _detsroyAnimation (self) -> None:
        """Animace smazání aktivity -> snižování opacity."""
        dt = 15
        width = self.winfo_width()
        if width > 0:
            self.configure(width = width)
            width = width - 5
            self.after(dt, self._detsroyAnimation)
        else:
            # smazání aktivity
            self.after(self.destroy_time, self.destroy)
