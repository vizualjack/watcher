import customtkinter
from seriesData.series import Series

root = None

def addLabel():
    global root
    label = customtkinter.CTkLabel(text="Here text", master=root)
    label.pack()


def newWindow():
    window = customtkinter.CTkToplevel()
    window.wm_title("new window")
    window.mainloop()

if __name__ == "__main__":
    series = [Series]
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    root = customtkinter.CTk()
    root.wm_title("Lol")
    addLabelBtn = customtkinter.CTkButton(master=root, text="Add label", command=addLabel)
    addLabelBtn.pack()
    newWindowBtn = customtkinter.CTkButton(master=root, text="Add window", command=newWindow)
    newWindowBtn.pack()
    root.mainloop()