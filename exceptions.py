from tkinter import *
from tkinter import ttk

def errorPopup(errorText):
    def errorclose():
        popup.destroy()
    popup = Tk()
    popup.title("Error")
    popup.attributes('-topmost', True)
    popup.resizable(False, False)
    popup.iconbitmap('Resources/favicon.ico')
    popupFrame = ttk.Frame(popup, padding=20)
    popupFrame.grid(column=0, row=0)
    pLabel = ttk.Label(popupFrame, text=errorText)
    pLabel.config(font=("TkDefaultFont", 10))
    pButton = ttk.Button(popupFrame, text="Ok", command=errorclose)
    pLabel.grid(sticky=W)
    pButton.grid(sticky=E, pady=(10,0))
    popup.mainloop()

class downloadNotFound(Exception):
    def __init__(self, message="No downloads folder found"):
        self.message = message
        errorPopup(message)

class noMiniDump(Exception):
    def __init__(self, message="No Minidump folder was found"):
        self.message = message
        errorPopup(message)

class fileDuplicate(Exception):
    def __init__(self, message="A file by that name is already created"):
        self.message = message
        errorPopup(message)

class noneSelected(Exception):
    def __init__(self, message="Please select at least one option"):
        self.message = message
        errorPopup(message)

class insufficientPermissions(Exception):
    def __init__(self, message="This program does not have the administrator privileges it needs to run"):
        self.message = message
        errorPopup(message)

class notWindows(Exception):
    def __init__(self, message="This program is meant for only Windows, an incompatible operating system was detected"):
        self.message = message
        errorPopup(message)

