# importovaní souborů
from addFrame import Frame as AddFrame
from menuFrame import Frame as MenuFrame
# import knihoven
import customtkinter as ctk

class App(ctk.CTk):
    """Třída pracující s hlavním oknem aplikace."""
    def __init__(self) -> None:
        """Inicializace hlavního kona aplikace."""
        super().__init__()
        self.title('Tréninkový deník')
        self.geometry('950x750')
        self.minsize(900, 600)
        self.load_main_gui()
        self.protocol('WM_DELETE_WINDOW', self._kill)
        self.addFrame
    
    def _kill(self):
        self.destroy()

    def load_main_gui(self) -> None:
        """Funkce tvořící SetFrame a AnimationFrame uvnitř okna."""
        self.addFrame = AddFrame(self)
        self.addFrame.pack(side=ctk.LEFT, fill=ctk.Y, ipadx=5, ipady=5, padx=3, pady=3)
        self.menuFrame = MenuFrame(self)
        self.menuFrame.configure(fg_color='transparent')
        self.menuFrame.pack(padx=3, pady=3, fill=ctk.BOTH, expand=True)
