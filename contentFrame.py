# import knihoven
import customtkinter as ctk
from tkinter import *
# import souborů
from overviewOption import Overview
from ctkWidgets import Button

class Frame (ctk.CTkFrame):
    """Obsahový frame - vybírá který vnitřní frame se zobrazí dále."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        
    def overviewOption(self):
        """Metoda pro zavolání možností pro záložku přehled."""
        # vytvoření instace s přehledem tréninků.
        Overview(self).pack(fill = ctk.BOTH, expand=True)

