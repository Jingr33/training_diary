# import knihoven
from tkinter import *
import customtkinter as ctk
from pywinstyles import set_opacity
# impor souborů
from ctkWidgets import Frame, Label
from general import General
from configuration import colors


class ConfirmAlert (Frame):
    """Vytvoří alert potvrzující úspěšné odstranění nebo úpravu tréninku v přehledu tréninků."""
    def __init__(self, master : ctk.CTkBaseClass):
        super().__init__(master)
        self.master = master
        self.height = 0
        self.label_height = 40

    def setAlertMessage (self, action : str) -> None:
        """Přidá zprávu do alert boxu s potvrzením o změně stavu tréninku."""
        text = self._makeMessage(action)
        self.configure(height = self.height + self.label_height)
        self.message = Label(self, text, ("Arial", 15))
        self.message.pack(side = TOP, fill = ctk.X, expand = True)
        self.message.configure(height = 40, corner_radius = 6)
        self._setLabelBackground(action)
        self._destroyInTime()

    def _makeMessage (self, action : str) -> str:
        """Vytvoří zpravu, která bude napsána v alertu."""
        if action == "update":
            action_text = "updatován"
        elif action == "delete":
            action_text = "odebrán"
        text = f"Trénink byl úspěšně {action_text}."
        return text
    
    def _setLabelBackground (self, action : str) -> None:
        """Nastaví pozadí framu v závisloti na provedené akci."""
        if action == "update":
            self.message.configure(fg_color = colors["dark-blue"])
        elif action == "delete":
            self.message.configure(fg_color = colors["dark-red"])

    def _destroyInTime (self) -> None:
        """Postupné automatické zničení framu s alertem."""
        self.message.bind("<Motion>", self._setDestroyTime)
        self.destroy_time = 4000
        self.opacity = 1
        self._destroyingProcess()

    def _destroyingProcess (self) -> None:
        """Funkce řídící postupné mizení a následné smazání framu, po určité době."""
        dt = 50
        if self.destroy_time > 0:
            if self.destroy_time <= 2000:
                self.opacity = self.opacity - 0.025
                set_opacity(self, value = self.opacity)
            self.destroy_time = self.destroy_time - dt
            self.after(dt, self._destroyingProcess)
        else:
            self._destroyFrameContent()

    def _setDestroyTime (self, value) -> None:
        """Nastaví čas, za který se smaže frame."""
        self.destroy_time = 3000
        self.opacity = 1
        set_opacity(self, value = self.opacity)

    def _destroyFrameContent (self) -> None:
        """Vymaže obsah framu a zmenší ho na nulu, ale nachá ho žít pro další použití."""
        General.deleteFrameWidgets(self)
        self.height = 0
        self.configure(fg_color = "transparent", height = self.height)