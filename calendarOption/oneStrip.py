# importy knihoven
from tkinter import *
import customtkinter as ctk
from CTkToolTip import *
# importy souborů
from ctkWidgets import Label

class OneStrip (Label):
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)
        