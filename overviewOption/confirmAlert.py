# import knihoven
from tkinter import *
import customtkinter as ctk
# impor souborů
from ctkWidgets import Frame


class ConfirmAlert (Frame):
    """Vytvoří alert potvrzující úspěšné odstranění nebo úpravu tréninku v přehledu tréninků."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
