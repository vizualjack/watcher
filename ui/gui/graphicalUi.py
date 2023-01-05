import customtkinter as ctk
from tracking.user import User
from seriesData.library import Library
from .listFrame import ListFrame
from .seriesFrame import SeriesFrame
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton,QWidget


# if pyinstaller doesnt work https://build-system.fman.io/pyqt5-tutorial
class GraphicalUI:
    def __init__(self, user:User, library:Library) -> None:
        self.user = user
        self.library = library
        self.app = QApplication([])
        self.rootWindow = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton('Top'))
        layout.addWidget(QPushButton('Bottom'))
        self.rootWindow.setLayout(layout)
        self.rootWindow.show()
        # ctk.set_appearance_mode("dark")
        # ctk.set_default_color_theme("blue")
        # self.rootWindow = ctk.CTk()
        # self.rootWindow.geometry("600x500")
        # self.rootWindow.wm_title('Watcher')
        # h = ctk.CTkScrollbar(self.rootWindow, button_color="green", button_hover_color="lightgreen", orientation='horizontal')
        # h.pack(side=ctk.BOTTOM, fill=ctk.X)
        # v = ctk.CTkScrollbar(self.rootWindow, button_color="green", button_hover_color="lightgreen")
        # v.pack(side=ctk.RIGHT, fill=ctk.Y)
        # # ctk.CTkButton(self.rootWindow, text='Switch', command=self.__switchWindow).pack()
        # self.currentFrame = ListFrame(self.rootWindow)
        # self.currentFrame.pack()
        # h.configure(True)
        # v.configure(True)

    def __switchWindow(self):
        pass
        # self.currentFrame.destroy()
        # if isinstance(self.currentFrame, ListFrame):
        #     self.currentFrame = SeriesFrame(self.rootWindow)
        # else:
        #     self.currentFrame = ListFrame(self.rootWindow)
        # self.currentFrame.pack()

    
    def use(self):
        self.app.exec()