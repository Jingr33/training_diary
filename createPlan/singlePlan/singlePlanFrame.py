# importy knihoven
from tkinter import *
import customtkinter as ctk
from datetime import date
from icecream import ic
#importy souborů
from createPlan.singlePlan.setDetailsFrame import SetDetailsFrame
from ctkWidgets import Frame, Label, Entry, ComboBox, CheckBox, Button
from general import General
from configuration import sport_list, days_in_week, single_plans_path

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
        self.date_entry = Entry(self, self.var_date)
        self.date_entry.grid(row = 2, column = 1, sticky = "W", pady = self.entry_pady)
        self.date_entry.configure(width = self.entry_width)
        # typ tréninku
        train_label = Label(self, "Trénink: ")
        train_label.grid(row = 3, column = 0, sticky = "E", padx = label_px)
        self.choose_train = StringVar(value = "nevybráno")
        self.train_cb = ComboBox(self, sport_list, self._initDetailFrame, self.choose_train)
        self.train_cb.grid(row = 3, column = 1, sticky = "W", pady = self.entry_pady)
        self.train_cb.configure(width = self.entry_width)
        # čas tréninku
        time_label = Label(self, "Čas:")
        time_label.grid(row = 4, column = 0, sticky = "E", padx = label_px)
        self.var_time = StringVar()
        self.time_entry = Entry(self, self.var_time)
        self.time_entry.grid(row = 4, column = 1, sticky = "W", pady = self.entry_pady)
        self.time_entry.configure(width = self.entry_width)
        # frame pro nastavení detailů
        self.detail_frame = SetDetailsFrame(self)
        self.detail_frame.grid(row = 5, column = 0, columnspan = 2, rowspan = 6, padx = (60, 5), pady = 15, sticky = "NSWE")
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
            cb_value = IntVar(value = 0)
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
        self.iter_entry = Entry (self, self.var_iter)
        self.iter_entry.grid(row = 3, column = 4)
        self.iter_entry.configure(width = self.entry_width)
        # jednou za počet dní
        cycle_lenght_label = Label(self, "Jednou za ... dní:")
        cycle_lenght_label.grid(row = 4, column = 4, sticky = "S")
        self.var_cycle_lenght = StringVar()
        self.cycle_lenght_entry = Entry(self, self.var_cycle_lenght)
        self.cycle_lenght_entry.grid(row = 5, column = 4)
        self.cycle_lenght_entry.configure(width = self.entry_width)

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
        # if (not self.terms["entries"][index].get()) and (not self.terms["entries"][index - 1].get()) and (index >= 1):
        #     self._removeTermsentry(index)
            
    def _initDetailFrame (self, value : str) -> None:
        """Vytvoří grafické rozhraní nastavování detailu tréninku podle zvoleného sportu."""
        self.detail_frame.initWidgets(value)

    def _savePlan (self) -> None:
        """Při kliknutí na tlačítko uložit zhodnotí správnost vstupů a plán do databáze."""
        checked = self._checkAllEntries()
        if checked:
            data_list = self._getEntryData()
            self._saveInDatabase(data_list)
            self._destroySelf()

    def _checkAllEntries (self) -> bool:
        """Funkce pro vyhodnocení správnosti všech vstupů."""
        date = self._checkMainDate()
        sport = self._checkSport()
        time = self._checkTime()
        details = self._checkDetailsFrameEntry(sport)
        repeat = self._checkRepeatEntries()
        other_terms = self._checkOtherTermsEntry()
        logical = self._checkLogicalEntry()
        if date and sport and time and details and repeat and other_terms and logical:
            return True
        return False

    def _checkMainDate (self) -> bool:
        """Zkontroluje platnost hlavního data, vrátí bool."""
        try:
            new_date = self.var_date.get()
            separator = General.findSeparator(new_date)
            if General.checkDateEntry(new_date, separator):
                General.setDefaultBorder(self.date_entry)
                return True
            else:
                General.setRedBorder(self.date_entry)
                return False
        except:
            General.setRedBorder(self.date_entry)
            return False
        
    def _checkSport (self) -> bool:
        """Zkontroluje platnost nastaveného sportu."""
        if self.choose_train.get() in sport_list:
            General.setDefaultBorder(self.train_cb)
            return True
        General.setRedBorder(self.train_cb)
        return False
    
    def _checkTime (self) -> bool:
        """Zkontroluje platnost nastaveného času tréninku."""
        time = self.var_time.get()
        if General.checkFloatEntry(time) or time == "":
            General.setDefaultBorder(self.time_entry)
            return True
        else:
            General.setRedBorder(self.time_entry)
            return False

    def _checkDetailsFrameEntry (self, sport_checked : bool) -> bool:
        """Zkontroluje vstupy detailů nastavení tréninku daného sportu (pokud je co kontrolovat)."""
        if sport_checked:
            return self.detail_frame.checkEntry()
        return False
    
    def _checkRepeatEntries (self) -> None:
        """Metoda ověří oba vstupy pro nastavení četnosti a častosti opakování tréninku."""
        iter = self._checkIterationEntry()
        freq = self._checkFrequencyEntry()
        if iter and freq:
            return True

    def _checkIterationEntry (self) -> bool:
        """Ověří vstup počtu iterací tréninku, vrátí bool."""
        if General.checkIntEntry(self.var_iter.get()) or self.var_iter.get() == "":
            General.setDefaultBorder(self.iter_entry)
            return True
        General.setRedBorder(self.iter_entry)
        return False

    def _checkFrequencyEntry (self) -> bool:
        """Ověří vstup častosti opakování tréninku, vrátí bool."""
        if General.checkIntEntry(self.var_cycle_lenght.get()) or self.var_cycle_lenght.get() == "":
            General.setDefaultBorder(self.cycle_lenght_entry)
            return True
        General.setRedBorder(self.cycle_lenght_entry)
        return False
    
    def _checkOtherTermsEntry (self) -> bool:
        """Ověří a obraví vstupy (podle spravnosti) nastavení dalšícho konkrétních dat tréninku."""
        for i in range(len(self.terms["vars"])):
            if self.terms["vars"][i].get() == "":
                return self._otherTermsBorderTrue(i)
            try:
                sep = General.findSeparator(self.terms["vars"][i].get())
                checked = General.checkDateEntry(self.terms["vars"][i].get(), sep)
                if checked:
                    return self._otherTermsBorderTrue(i)
                else:
                    return self._otherTermsBorderFalse(i)
            except:
                return self._otherTermsBorderFalse(i)
            
    def _otherTermsBorderTrue (self, index : int) -> bool:
        General.setDefaultBorder(self.terms["entries"][index])
        return True
    
    def _otherTermsBorderFalse (self, index : int) -> bool:
        General.setRedBorder(self.terms["entries"][index])
        return False
    
    def _checkLogicalEntry (self) -> bool:
        """Vrátí bool, kontroluje, zda jsou zadané všechnx potřebné parametry pro zapsání dat do souboru."""
        days_in_week = False
        for value in self.cb_values:
            if value.get() != 0:
                days_in_week = True
                break
        if (days_in_week or self.var_cycle_lenght.get()) and (not self.var_iter.get()):
            General.setRedBorder(self.iter_entry)
            return False
        General.setDefaultBorder(self.iter_entry)
        return True
    
    def _getEntryData (self) -> list:
        """Získá data zadaná uživatel jako list datumů a list podrobností tréninku. Vrátí jako 2d list [data, podrobnosti]."""
        train_details = self._getTrainingData()
        terms = self._getDates()
        return [terms, train_details]

    def _getTrainingData (self) -> list:
        """Získá data o tréninku. Vrátí list dat, který bude tvořit 1 řádek v souboru s tréninkovými plány."""
        sport_line = [self.choose_train.get(), self.var_time.get()]
        sport_line.extend(self.detail_frame.getData())
        return sport_line

    def _getDates (self) -> list:
        """Získá data, ve kterých se trénink zopakuje. Vrátí list těchto dat pro zapsání jednoho řádku do souboru databáze sinle plánů."""
        main_date = General.stringToDate(self.var_date.get())
        date_line = [main_date] # hlavní datum
        date_line.extend(self._getOtherTerms()) # přidaní konkrétních dat
        if self.var_cycle_lenght.get() != "":
            date_line.extend(self._getRepeatingDates(main_date)) # přádaní cyklů
        date_line.extend(self._getInWeekRepeat(main_date, self.var_iter.get())) # dny v týdnu
        date_line.sort()
        date_line = self._changeToDatabaseDate(date_line)
        return date_line

    def _getOtherTerms (self) -> list:
        """Vrátí list datumů získaných z části zadávání konkrétních data tréninku."""
        dates = []
        for i in range(len(self.terms["vars"])):
            if self.terms["vars"][i].get() == "": continue
            other_date = General.stringToDate(self.terms["vars"][i].get())
            dates.append(other_date)
        return dates

    def _getRepeatingDates (self, start_date : date) -> list:
        """Vrátí list datumů s části zadávání frekvence a počtu opakování tréninku."""
        dates = [None] * int(self.var_iter.get())
        for i in range(int(self.var_iter.get())):
            days = int(self.var_cycle_lenght.get())
            next_date = General.surroundingFirstDate(start_date, 0, 0, (i + 1)*days)
            dates[i] = next_date
        return dates
    
    def _getInWeekRepeat (self, start_date : date, repetition : str) -> list:
        """Pokud jsou iterace zadány, vrátí list datumů získaných z části opakování tréninků v týdnu."""
        if not General.checkIntEntry(repetition):
            return []
        repetition = int(repetition)
        if self._checkEmptyWeek():
            return []
        dates = []
        for day_of_week in range(len(self.cb_values)):
            if self.cb_values[day_of_week].get() == 0: continue #den nebyl nastaven -> přeskočí se
            dates.extend(self._dayOfWeekDayDates(start_date, day_of_week, repetition))
        return dates
    
    def _checkEmptyWeek (self) -> None:
        """Zkontroluje, zda bylo něco zadání do nastavení opakování tréninků v jednotlivých dnech v týdnu."""
        for value in self.cb_values: # pokud není zadán žádný den v týdnu
            if value.get() == 1:
                return False
        return True

    def _dayOfWeekDayDates (self, start_date : date, day_in_week : int, repetition : int) -> list:
        """Vrátí pro každý den v týdnu list dat, ve kterých se trénink zopakuje."""
        start_date_day = start_date.weekday()
        first_repeat = day_in_week - start_date_day # za kolik dní od počátku nastane první opakování tréninku
        if day_in_week < start_date_day: # pokud je první opakování před počátečním datem, bude o  týden později
            first_repeat = first_repeat + 7
        dates = [General.surroundingFirstDate(start_date, 0, 0, first_repeat)]
        for i in range(1, repetition):
            dates.append(General.surroundingFirstDate(dates[0], 0, 0, i*7))
        return dates
    
    def _changeToDatabaseDate (self, date_list : list) -> None:
        for i in range(len(date_list)):
            date_list[i] = General.changeDateForamt(date_list[i])
        return date_list
    
    def _saveInDatabase (self, data_list : list) -> None:
        """Uloží data do databáze jednoduchých tréninkových plánu."""
        for i in range(len(data_list)):
            data_list[i] = General.prepareString(data_list[i])
        with open (single_plans_path, 'a') as f:
            f.seek(2)
            for line in data_list:
                f.write(line +  " / \n")
            f.write(";\n")

    def _destroySelf (self) -> None:
        """Zavře toto okno i kono výběru plánu."""
        self.master.backToChoiceWindow()
        self.master.master.kill()