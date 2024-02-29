# importy knihoven
from tkinter import *
import customtkinter as ctk
#importy souborů
from createPlan.singlePlan.setDetailsFrame import SetDetailsFrame
from ctkWidgets import Frame, Label, Entry, ComboBox, CheckBox, Button
from general import General
from configuration import sport_list, days_in_week

class SinglePlanFrame (Frame):
    """Frame s nastavení single tréninkového plánu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.term_entry_index = 0
        self.title_height = 40
        self.entry_pady = 7
        self.cb_pady = 9
        # nastavení mřížky
        self.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)
        self.rowconfigure([0, 2, 3, 4, 5, 6, 7, 8, 9], weight = 0)
        self.rowconfigure(10, weight = 5)
        # vytvoření widget
        General.initBackButton(self)
        self._initSetTrainColumns()
        self._initIterationColumns()
        self._initSavebutton()

    def _initSetTrainColumns (self) -> None:
        """Vytvoření widget pro natavení nového tréninku a jeho podrobností."""
        label_px = 5
        self.entry_width = 100
        # label s nadpisem
        title1_label = Label(self, "Trénink", ("Arial", 15, 'bold'))
        title1_label.grid(row = 1, column = 0, columnspan = 2)
        title1_label.configure(height = self.title_height)
        # datum
        date_label = Label(self, "Datum: ")
        date_label.grid(row = 2, column = 0, sticky = "E", padx = label_px)
        self.var_date = StringVar()
        date_entry = Entry(self, self.var_date)
        date_entry.grid(row = 2, column = 1, sticky = "W", pady = self.entry_pady)
        date_entry.configure(width = self.entry_width)
        # typ tréninku
        train_label = Label(self, "Trénink: ")
        train_label.grid(row = 3, column = 0, sticky = "E", padx = label_px)
        self.choose_train = sport_list[0]
        train_cb = ComboBox(self, sport_list, self._initDetailFrame, self.choose_train)
        train_cb.grid(row = 3, column = 1, sticky = "W", pady = self.entry_pady)
        train_cb.configure(width = self.entry_width)
        # frame pro nastavení detailů
        self.detail_frame = SetDetailsFrame(self)
        self.detail_frame.grid(row = 4, column = 0, columnspan = 2, rowspan = 6, padx = (60, 5), pady = 15, sticky = "NSWE")
        self.detail_frame.configure(width = 200, height = 200, fg_color = "transparent")

    def _initIterationColumns (self) -> None:
        """Vytvoří widgety pro nastavení opakování tréninků."""
        # nadpis
        title2_label = Label(self, "Opakování", ("Arial", 15, "bold"))
        title2_label.grid(row = 1, column = 3, columnspan = 4)
        title2_label.configure(height = self.title_height)
        # další widgety
        self._initDaysInWeek()
        self._initIterationNumber()
        self._initParticularDates()

    def _initDaysInWeek (self) -> None:
        """Vytvoří wigety pro nastavení opakování v jednotlivých dnech v týdnu."""
        padx = 5
        # nadpis
        week_title = Label(self, "Dny v týdnu:")
        week_title.grid(row = 2, column = 3, padx = padx)
        # dny v týdnu
        self.cb_values = [None] * 7
        self.checkboxes = [None] * 7
        for i in range(0, 7):
            cb_value = IntVar()
            checkbox = CheckBox(self, days_in_week[i], cb_value)
            checkbox.grid(row = 3+i, column = 3, padx = padx, pady = self.cb_pady)
            self.cb_values[i] = cb_value
            self.checkboxes[i] = checkbox

    def _initIterationNumber (self) -> None:
        """Vytvoří widgety pro natavení počtu opakování a "častosti" opakování."""
        # počet opakování
        iter_label = Label(self, "Počet opakování")
        iter_label.grid(row = 2, column = 4)
        self.var_iter = StringVar()
        iter_entry = Entry (self, self.var_iter)
        iter_entry.grid(row = 3, column = 4)
        iter_entry.configure(width = self.entry_width)
        # jednou za počet dní
        cycle_lenght_label = Label(self, "Jednou za ... dní:")
        cycle_lenght_label.grid(row = 4, column = 4, sticky = "S")
        self.var_cycle_lenght = StringVar()
        cycle_lenght_entry = Entry(self, self.var_cycle_lenght)
        cycle_lenght_entry.grid(row = 5, column = 4)
        cycle_lenght_entry.configure(width = self.entry_width)

    def _initParticularDates (self) -> None:
        """Vytvoří widgety pro nastavení jednotlivých dat tréninků."""
        # nadpis
        terms_label = Label(self, "Konkrétní data:")
        terms_label.grid(row = 2, column = 5, columnspan = 2)
        # zadaná druhého data (prvního v pořadí)
        self.term_entry_index = 0
        self.terms = {
            "labels" : [],
            "entries" : [],
            "vars" : [],
        }
        self._addTermsEntry(self.term_entry_index)

    def _initSavebutton (self) -> None:
        """Vytvoří tlačítko pro uložení plánu v dolní části okna."""
        save_button = Button(self, "Uložit", self._savePlan)
        save_button.grid(column = 5, row = 10, columnspan = 2, padx = 10, pady = 10, sticky = "SE")
        save_button.configure(height = 40, width = 150)

    def _addTermsEntry (self, index : int) -> None:
        """Vytvoří další entry a label (s číslem) pro zadaní konkrétního dalšího data tréninku."""
        term_label = Label(self, str(index + 2) + ". ")
        term_label.grid(row = index + 3, column = 5, sticky = "E", padx = 5)
        var_term = StringVar()
        term_entry = Entry(self, var_term)
        term_entry.grid(row = index + 3, column = 6, pady = self.entry_pady, padx = 5)
        term_entry.configure(width = self.entry_width)
        term_entry.bind("<FocusIn>", lambda value: self._regenerateTermEntry(index))
        if index >= 2:
            self.terms["entries"][index - 2].unbind("<FocusIn>")
        self.terms["labels"].append(term_label)
        self.terms["entries"].append(term_entry)
        self.terms["vars"].append(var_term)

    def _removeTermsentry (self, index : int) -> None:
        """Odebere poslední entry a label (s číslem) pro zadání konkrétního dalšího data tréninku."""
        # self.terms["entries"][-1].unbind("<Key>")
        # self.terms["entries"][-3].bind("<Key>", lambda value: self._regenerateTermEntry(index - 1))
        # self.terms["labels"][-1].destroy()
        # self.terms["entries"][-1].destroy()
        # del self.terms["labels"][-1]
        # del self.terms["entries"][-1]
        # del self.terms["vars"][-1]

    def _regenerateTermEntry (self, index : int) -> None:
        """Upraví počet řádků pro zapsání termínu nového tréninku."""
        if index <= 5:
            self._addTermsEntry(index + 1)
        # print(self.terms["entries"][index].get())
        # print(self.terms["entries"][index - 1].get())
        # if (not self.terms["entries"][index].get()) and (not self.terms["entries"][index - 1].get()) and (index >= 1):
        #     self._removeTermsentry(index)
            
    def _initDetailFrame (self, value : str) -> None:
        """Vytvoří grafické rozhraní nastavování detailu tréninku podle zvoleného sportu."""
        self.detail_frame.initWidgets(value)

    def _savePlan (self) -> None:
        """Uložení plánu."""
        ...