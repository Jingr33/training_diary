# importy knihoven
from tkinter import *
import customtkinter as ctk
#importy souborů
from ctkWidgets import Frame, Label

class SinglePlanFrame (Frame):
    """Frame s nastavení single tréninkového plánu."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        Label(self, "label")
