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
            #label
            sport_name = Label(self, sport_list[i], ("Arial", 14, "normal"))
            sport_name.grid(row = i, column = 0, sticky = ctk.W, padx = padx_label, pady = pady)
            #checkbox
            cb_var = IntVar()
            cb_var.set(GV.selected_sports[i])
            select_cb = CheckBox(self, "", cb_var)
            select_cb.grid(row = i, column = 1, padx = padx_cb, pady = pady)
            select_cb.configure(width = 27, fg_color = GV.sport_colors[sport_list[i]], command = lambda: self._setSelectedSports(i))
            checkboxes[i] = select_cb
            vars[i] = cb_var
            # button
            choose_color = Button(self, "Změnit barvu", lambda: self._initColorPicker(i))
            choose_color.grid(row = i, column = 2, pady = pady)
            choose_color.configure(width = 100, height = 27, fg_color = GV.sport_colors[sport_list[i]])
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
            self.sport_widgets["checkbox"][index].configure(fg_color = color)
            GV.sport_colors[sport_list[index]] = color
            GV.overwriteSettingFile()

    def _setSelectedSports(self, index : int) -> None:
        """Nastaví změny ve vybraných sportech, uloží nastavení do databáze."""
        changed_value = int(self.sport_widgets["var"][index].get())
        GV.selected_sports[index] = changed_value
        self._changeStateOfButton(changed_value, index)
        GV.overwriteSettingFile()

    def _changeStateOfButton (self, changed_value : int, index : int) -> None:
        """Změní nastavení stavu tlačítka pro výběr barvy na disabled v případě, že sport není vybrán."""
        if changed_value:
            self.sport_widgets["button"][index].configure(state = "normal")
        else:
            self.sport_widgets["button"][index].configure(state = "disabled")
