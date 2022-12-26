import customtkinter as ctk
from tracking.user import User
from seriesData.library import Library
from .listFrame import ListFrame
from .seriesFrame import SeriesFrame



class GraphicalUI:
    def __init__(self, user:User, library:Library) -> None:
        self.user = user
        self.library = library
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.rootWindow = ctk.CTk()
        self.rootWindow.wm_title('Watcher')
        ctk.CTkButton(self.rootWindow, text='Switch', command=self.__switchWindow).pack()
        self.currentFrame = ListFrame(self.rootWindow)
        self.currentFrame.pack()
        # self.rootWindow.resizable(0, 0)


    def __switchWindow(self):
        self.currentFrame.destroy()
        if isinstance(self.currentFrame, ListFrame):
            self.currentFrame = SeriesFrame(self.rootWindow)
        else:
            self.currentFrame = ListFrame(self.rootWindow)
        self.currentFrame.pack()

    
    def use(self):
        self.rootWindow.mainloop()