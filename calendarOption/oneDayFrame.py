# importy knihoven
from tkinter import *
import customtkinter as ctk
# importy souborů
from ctkWidgets import Frame


class OneDayFrame (Frame):
    """Frame pro vyobrazení jednoho dne v grafickém kalendáři."""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)