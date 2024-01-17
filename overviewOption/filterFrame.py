# import knihoven
from tkinter import *
import customtkinter as ctk
from ctkWidgets import Frame, CheckBox, Label, Entry, Button
from overviewOption.filter import Filter
from configuration import sport_list, gym_body_parts


class FilterFrame (ctk.CTkFrame):
    """Vytvoří Frame pro zaklikávání možností filtrování v přehledu tréninků."""
    def __init__(self, master :ctk.CTkBaseClass, trainings):
        super().__init__(master)
        self.trainings = trainings

        # vytvoření grafického rozhraní
        self._createGUI()

        # eventy pro přidávání a oddělávání podrobného nastavení
        self.filter_sport.gym_chb.bind('<Button-1>', self.gymFilterSelected)
        self.filter_sport.run_chb.bind('<Button-1>', self.runFilterSelected)

    def _createGUI(self):
        """Vytvoření grafického rozraní."""
        self.filter_date = FilterDate(self)
        self.filter_date.pack(side=LEFT, fill=ctk.Y, ipadx=3)
        self.filter_date.configure(width = 100, height=100, corner_radius = 0, fg_color='transparent')

        self.filter_sport = FilterSport(self)
        self.filter_sport.pack(side=LEFT, fill=ctk.Y, ipadx=3)
        self.filter_sport.configure(width = 110, height=100, corner_radius = 0, fg_color='transparent')

        self.filter_time = FilterTime(self)
        self.filter_time.pack(side=LEFT, fill=ctk.Y, ipadx=3)
        self.filter_time.configure(width = 80, height=100, corner_radius = 0, fg_color='transparent')

        self.filter_details = FilterDetails(self)
        self.filter_details.pack(side=LEFT, fill = ctk.Y, ipadx=3, padx=10)
        self.filter_details.configure(width = 250, height=100, corner_radius = 0, fg_color='transparent')

        self.filter_button = Button(self, "Filtrovat", self._filter)
        self.filter_button.pack(side=RIGHT, ipadx=7, ipady=7, anchor=ctk.N, padx=10, pady=10)
        self.filter_button.configure(width=70)


    def _filter(self):
        """Spuštění filtrování při kliknutí na tlačítko filtrovat."""
        #TODO - stažení hodnot o filtrování data
        date_filter = ""

        # stažení hodnot filtrování sportu
        sport_filter = self.filter_sport.filtered()

        # stažení hodnot o filtrování času
        time_filter = self.filter_time.filtered()

        # zavolání vyfiltrování
        self.filter = Filter(self.trainings, date_filter, sport_filter, time_filter)
        self.filtered_data = self.filter.getFilteredData()

    def getData (self):
        """Metoda vrátí vyfiltrovaná data."""
        return self.filtered_data
    
    def gymFilterSelected (self, master):
        """Metoda pro přidání podrobného nastavení pro tréninky v posilovně."""
        if int(self.filter_sport.var_gym.get()) == 0:
            # destroyne widgety posilovny
            for widget in self.filter_details.gym_details_widgets:
                widget.destroy()
            self.filter_details.details_rows = self.filter_details.details_rows - self.filter_details.gym_rows
        elif int(self.filter_sport.var_gym.get()) == 1:
            self.filter_details.createGym()
            self.filter_details.details_rows = self.filter_details.details_rows + self.filter_details.gym_rows

        self.runFilterSelected() # zavolání ostatních detailních filtrů pro vyrenderování

    def runFilterSelected (self):
        """Metoda pro přidání podrobného nastavení pro běžecké tréninky."""
        ... #TODO


class FilterDate (Frame):
    """Frame pro filtrování data."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)

        #TODO - filtrování data

class FilterSport (Frame):
    """Frame pro filtrování sportu."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.var_gym = StringVar(value=1)
        self.var_run = StringVar(value=1)

        #vytvoření checkboxů pro zakliknnutí sportu
        self.gym_chb = CheckBox(self, sport_list[0], self.var_gym)
        self.gym_chb.pack(side=TOP, pady=1)
        self.gym_chb.select()
        self.run_chb = CheckBox(self, sport_list[1], self.var_run)
        self.run_chb.pack(side=TOP, pady=1)
        self.run_chb.select()

    def filtered(self):
        """Vrátí hodnoty zakliknuté ve filtru sportu."""
        values = [self.var_gym.get(), self.var_run.get()]
        return values


class FilterTime (Frame):
    """Frame pro filtrování času."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.var_from = StringVar()
        self.var_to = StringVar()

        # vytvoření zadávacích polí pro filtrování času
        from_l = Label(self, "Od:")
        from_l.grid(row = 0, column = 0)
        from_l.configure(font= ("Arial", 12))
        from_e = Entry(self, self.var_from)
        self.var_from.set("0")
        from_e.grid(row=0, column=1, ipadx=2, ipady=1)
        from_e.configure(width = 35)

        to_l = Label(self, "Do:")
        to_l.grid(row=1, column=0)
        to_l.configure(font= ("Arial", 12))
        to_e = Entry(self, self.var_to)
        self.var_to.set(999)
        to_e.grid(row=1, column=1, ipadx=2, ipady=1)
        to_e.configure(width = 35)

    def filtered(self):
        """Vrátí hodnoty zakliknuté ve filtru času."""
        values = [self.var_from.get(), self.var_to.get()]
        return values

class FilterDetails (Frame):
    """Frame pro filtrování detailnějšího nastavení podle zvoleného sportu."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        self.details_rows = 0
        # proměná pro zabírání řádků v mřížce
        self.gym_rows = 2
        # proměnná pro zabírání řádků v mřížce
        self.run_rows = 1



        self.createGym()

        self.details_rows = self.gym_rows
        self.createRun()

    def createGym(self):
        """Metoda pro vytvoření grafiky pro filtraci jednotlivých části těla."""

        # inicializace grafiky
        self.label = Label(self, "Části těla: ", font=("Arial", 10))
        self.label.grid(row = self.details_rows, column=0)

        self.leg_b = Button(self, gym_body_parts[0], ...)
        self.leg_b.grid(row = self.details_rows, column = 1, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.leg_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W)

        self.core_b = Button(self, gym_body_parts[1], ...)
        self.core_b.grid(row = self.details_rows, column = 2, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.core_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W)

        self.breast_b = Button(self, gym_body_parts[2], ...)
        self.breast_b.grid(row = self.details_rows, column = 3, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.breast_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W)

        self.shoulders_b = Button(self, gym_body_parts[3], ...)
        self.shoulders_b.grid(row = self.details_rows, column = 4, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.shoulders_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W)

        self.back_b = Button(self, gym_body_parts[4], ...)
        self.back_b.grid(row = self.details_rows+1, column = 1, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.back_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W)

        self.biceps_b = Button(self, gym_body_parts[5], ...)
        self.biceps_b.grid(row = self.details_rows+1, column = 2, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.biceps_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W)

        self.triceps_b = Button(self, gym_body_parts[6], ...)
        self.triceps_b.grid(row = self.details_rows+1, column = 3, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.triceps_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W)

        self.forearm_b = Button(self, gym_body_parts[7], ...)
        self.forearm_b.grid(row = self.details_rows+1, column = 4, padx = 1, pady = 0, ipadx=0, ipady=0)
        self.forearm_b.configure(font=("Arial", 10), height = 15, width = 20, anchor=ctk.W)

        # pole všech grafických objektů funkce
        self.gym_details_widgets = [self.label, self.leg_b, self.core_b, self.breast_b, self.shoulders_b,
                               self.back_b, self.biceps_b, self.triceps_b, self.forearm_b]

    def createRun(self):
        """Metoda pro vytvoření grafiky pro filtraci distance běhu."""

        self.var_from = StringVar()
        self.var_to = StringVar()

        self.run_l = Label(self, "Běh délka:", ("Arial", 10))
        self.run_l.grid(row=self.details_rows, column=0)

        self.from_l = Label(self, "Od:", ("Airal", 10))
        self.from_l.grid(row = self.details_rows, column = 1)

        self.from_e = Entry(self, self.var_from)
        self.from_e.grid(row=self.details_rows, column = 2)
        self.from_e.configure(height = 20, width=35)

        self.to_l = Label(self, "Do:", ("Airal", 10))
        self.to_l.grid(row = self.details_rows, column = 3)

        self.to_e = Entry(self, self.var_from)
        self.to_e.grid(row=self.details_rows, column = 4)
        self.to_e.configure(height = 20, width=35)

        # pole všech grafických objektů funkce
        self.run_details_widgets = [self.run_l, self.from_l, self.from_e,
                                    self.to_l, self.to_e]




