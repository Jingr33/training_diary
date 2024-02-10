#import knihoven
from PIL import Image as img
from tkinter import *
import customtkinter as ctk

class Image (ctk.CTkImage):
    """Třída tvořící obrázky do grafického rozhraní."""
    def __init__(self, dark_image :str, size : tuple):
        dark_image = img.open(dark_image)
        super().__init__(None, dark_image, size)