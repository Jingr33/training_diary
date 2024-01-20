# import knihoven
import customtkinter as ctk
from tkinter import *
# import souborů
from calendarOption.oneDayFrame import OneDayFrame

class calendarTable (ctk.CTkScrollableFrame):
    """Vytvoří grafický kalendář jako čtvercovou soustavu framů."""
    def __init__(self, master :ctk.CTkBaseClass, date : tuple):
        super().__init__(master)

        # inicializace framové mřížky
        self._initGrid()


    def _initGrid(self) -> None:
        """Metoda pro vytvoření framové mřížky (6 řádků, 7 sloupců)."""
        # 6 řádků, protože do více týdnů 1 měsíc nikdy nezasahuje
        for row in range(6): #přes řádky
            for column in range(7): #přes sloupce
                frame = OneDayFrame(self)
                frame.grid(row=row, column=column)
                frame.configure(height = 100, width = 100, corner_radius = 0)

        #TODO
        # uprav ať s to roztahuje při resizování
        # ukládej framy do nějkých polí, ať s tím pak můžeš pracovat nějak