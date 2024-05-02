# importy knihoven
import customtkinter as ctk
from tkinter import *

class Button(ctk.CTkButton):
    """Třída pro tvorbu ctk.Button"""
    def __init__(self, master: ctk.CTkBaseClass, text: str, command):
        super().__init__(master)
        self.configure(text=text, command=command)

class Label(ctk.CTkLabel):
    """Třída pro tvorbu ctk.Label"""
    def __init__(self, master: ctk.CTkBaseClass, name: str, font = ("Arial", 13) ):
        super().__init__(master)
        self.configure(text=name, font=font)

class Entry(ctk.CTkEntry):
    """Třída pro tvorbu ctk.Entry"""
    def __init__(self, master: ctk.CTkBaseClass, value):
        super().__init__(master)
        self.configure(textvariable = value)

class ComboBox(ctk.CTkComboBox):
    """Třída pro tvorbu ctk.ComboBox"""
    def __init__(self, master: ctk.CTkComboBox, options, command, initial_variable):
        super().__init__(master)
        self.configure(values = options, command = command, variable = initial_variable)

class CheckBox(ctk.CTkCheckBox):
    """Třída pro tvorbu ctk.CTkCheckBox"""
    def __init__(self, master: ctk.CTkCheckBox, text: str, variable):
        super().__init__(master)
        self.configure(text=text, variable=variable)

class TabView(ctk.CTkTabview):
    """Třída pro tvorbu ctk.CTkTabView."""
    def __init__(self, master :ctk.CTkTabview):
        super().__init__(master)

class SegmentedButton(ctk.CTkSegmentedButton):
    """Třída pro tvorbu ctk.CTkSegmentedButton."""
    def __init__(self, master :ctk.CTkSegmentedButton, values :list, command):
        super().__init__(master)
        self.configure(values = values, command = command)

class Frame (ctk.CTkFrame):
    """Třída pro tvorbu ctk.CTkFrame"""
    def __init__(self, master :ctk.CTkBaseClass):
        super().__init__(master)

class Scrollbar (ctk.CTkScrollbar):
    """Scrollbar widget."""
    def __init__(self, master :ctk.CTkBaseClass, command):
        super().__init__(master)
        self.configure(command=command)

class Switch (ctk.CTkSwitch):
    """Switch widget."""
    def __init__(self, master : ctk.CTkBaseClass, text, command, variable):
        super().__init__(master)
        self.configure(text=text, command=command, variable=variable)