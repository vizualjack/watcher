from typing import Optional, Tuple, Union
import customtkinter as ctk
from PIL import Image, ImageTk


class ListEntryFrame(ctk.CTkFrame):
    def __init__(self, master: any, width: int = 300, height: int = 425, corner_radius: Optional[Union[int, str]] = None, border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent", fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None, background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None, overwrite_preferred_drawing_method: Union[str, None] = None, **kwargs):
        scale = 0.75
        width = int(width*scale)
        height = int(height*scale)
        corner_radius = 10
        # fg_color = "red"
        bg_color = "transparent"
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # background image
        image1 = Image.open("./image.webp")
        ctkImage = ctk.CTkImage(image1, size=(width, height))
        imageHolder = ctk.CTkLabel(self, image=ctkImage,text="")
        imageHolder.pack()

        label = ctk.CTkLabel(self, text='Title')
        label.pack()