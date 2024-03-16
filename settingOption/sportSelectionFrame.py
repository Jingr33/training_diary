# import knihoven
from tkinter import *
import customtkinter as ctk
from CTkColorPicker import *
from icecream  import ic
# import souborů
from ctkWidgets import Frame, Label, Button, CheckBox
from configuration import sport_list
import globalVariables as GV


class SportSelectionFrame (Frame):
    """Vytvoří frame pro vybraní nebo odebraání sportů v nastavení aplikace."""
    def __init__(self, master : ctk.CTkBaseClass):
        self.master = master
        super().__init__(master)
        self.configure(fg_color = "transparent")
        self._initWidgets()

    def _initWidgets (self) -> None:
        """Vytvoří widgety framu."""
        padx_label = (10, 3)
        padx_cb = 3
        pady = 2
        checkboxes = [None] * len(sport_list)
        buttons = [None] * len(sport_list)
        vars = [None] * len(sport_list)
        for i in range(len(sport_list)):
            sport_name = Label(self, sport_list[i], ("Arial", 14, "normal"))
            sport_name.grid(row = i, column = 0, sticky = ctk.W, padx = padx_label, pady = pady)
            cb_var = IntVar()
            select_cb = CheckBox(self, "", cb_var)
            select_cb.grid(row = i, column = 1, padx = padx_cb, pady = pady)
            select_cb.configure(width = 27)
            checkboxes[i] = select_cb
            vars[i] = cb_var
            choose_color = Button(self, "Změnit barvu", lambda: self._initColorPicker(i))
            choose_color.grid(row = i, column = 2, pady = pady)
            choose_color.configure(width = 100, height = 27)
            buttons[i] = choose_color
        # slovník potřebných widgetů
        self.sport_widgets = {
            "checkbox" : checkboxes,
            "var" : vars,
            "button" : buttons,
        }

    def _initColorPicker (self, index : int) -> None:
        """Iniciuje okno s vyběrem barvy k odpovídajícímu tlačítku pro nastavení barvy."""
        pick_color = AskColor(title="Nastavení barvy", text="Vybrat")
        color = pick_color.get()
        if color:
            self.sport_widgets["button"][index].configure(fg_color = color)
            self.sport_widgets["checkbox"] [index].configure(fg_color = color)
            GV.sport_colors[sport_list[index]] = color
            ic(GV.sport_colors)
            GV.overwriteSettingFile()