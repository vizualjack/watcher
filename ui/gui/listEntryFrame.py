from typing import Optional, Tuple, Union
import customtkinter as ctk


class ListEntryFrame(ctk.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None, border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent", fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None, background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None, overwrite_preferred_drawing_method: Union[str, None] = None, **kwargs):
        fg_color = "red"
        bg_color = "green"
        corner_radius = 20
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        # background = ctk.CTkFrame(self, corner_radius=20, bg_color="red", fg_color="green")
        # background.pack()
        label = ctk.CTkLabel(self, text='Title')
        label.pack()
