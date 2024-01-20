#importy knihoven
import customtkinter as ctk
from tkinter import *
#importy souborů
from ctkWidgets import SegmentedButton
from configuration import menu_list
from contentFrame import Frame as ContentFrame

class Frame (ctk.CTkFrame):
    """Frame pro výběr z možností základního menu."""
    def __init__(self, master: ctk.CTkBaseClass):
        super().__init__(master)
        # vytvoření proměnných pro instance jednotlivých oken
        self.contentFrames = [None] * len(menu_list)

        # vytvoření segmentovaného buttonu
        seg_button = SegmentedButton(self, menu_list, self.optionSelected)
        seg_button.configure(font = ("Arial", 13), height = 45)
        seg_button.pack(fill = ctk.X, side=TOP)

        self.content_frame = ContentFrame(self)
        self.content_frame.pack(ipadx = 5, ipady = 5, expand = True, fill = ctk.BOTH)


    def optionSelected (self, option):
        """Metoda spustí frame podle zvolené možnosti v segment buttonu."""
        if option == menu_list[0]:
            # smazaní předchozího obsahu
            self._oldWidgetsDestroy()
            # vytvoření obsahu framu
            self.content_frame.overviewOption()

        elif option == menu_list[1]:
            # smazaní předchozího obsahu
            self._oldWidgetsDestroy()
            # vytvoření obsahu framu
            self.content_frame.calendarOption()

        elif option == menu_list[2]:
            ... #TODO

    def _oldWidgetsDestroy(self):
        """Metoda vymaže obsah contentFramu, při přepnutí na jinou záložku."""
        # smazání předchozího obsahu
        for widget in self.content_frame.winfo_children():
            widget.destroy()
