import subprocess
import os
from tkinter import *
from tkinter import ttk
import shutil
import zipfile
from datetime import datetime

from exceptions import *

user = os.getlogin()

filename = datetime.now().strftime('%m%d%Y-%I%M%S%p-System-Information-Files')

#UI Elements
root = Tk()
root.resizable(False, False)
root.iconbitmap('Resources/favicon.ico')
frame = ttk.Frame(root, padding=20)
frame.grid(column=0, row=0)

crashFiles = BooleanVar(root, False)
hardwareInfo = BooleanVar(root, False)
osInfo = BooleanVar(root, False)
driverInfo = BooleanVar(root, False)
usbDevices = BooleanVar(root, False)

root.title("System Information Tool")

def crash():
    print("Checking for Downloads folder")
    downloadsPath = "None"
    if os.path.exists(rf"C:\Users\{user}\Downloads"):
        downloadsPath = rf"C:\Users\{user}\Downloads"
    elif os.path.exists(rf"C:\Users\OneDrive\{user}\Downloads"):
        downloadsPath = rf"C:\Users\OneDrive\{user}\Downloads"
    else:
        raise downloadNotFound
    print("Downloads folder found")

    print("Checking for Minidumps folder")
    if os.path.exists(r"C:\Windows\Minidump"):
        pass
    else:
        raise noMiniDump
    print("Minidump folder found")

    try:
        shutil.copytree(r"C:\Windows\Minidump", rf"{downloadsPath}\{filename}\Minidumps")
    except FileExistsError:
        raise fileDuplicate

def hardware():
    print("Hi")

def windowsos():
    print("Hi")

def drivers():
    print("Hi")

def usb():
    print("Hi")

def optionsFalse():
    falseOptions = 0
    if not crashFiles.get():
        falseOptions = falseOptions + 1
    if not hardwareInfo.get():
        falseOptions = falseOptions + 1
    if not osInfo.get():
        falseOptions = falseOptions + 1
    if not driverInfo.get():
        falseOptions = falseOptions + 1
    if not usbDevices.get():
        falseOptions = falseOptions + 1
    if falseOptions == 5:
        return False
    else:
        return True

def runFunction():
    if crashFiles.get():
        crash()
    if hardwareInfo.get():
        hardware()
    if osInfo.get():
        windowsos()
    if driverInfo.get():
        drivers()
    if usbDevices.get():
        usb()
    elif not optionsFalse():
        raise noneSelected

label1 = ttk.Label(frame, text="Please choose below what you would like to be packaged into the .zip file:")
label1.config(font=("TkDefaultFont", 11))
option1 = ttk.Checkbutton(frame, text="Minidump/Crash Files", variable=crashFiles, onvalue=True, offvalue=False)
option2 = ttk.Checkbutton(frame, text="Hardware Information", variable=hardwareInfo, onvalue=True, offvalue=False)
option3 = ttk.Checkbutton(frame, text="Windows Operating System Information", variable=osInfo, onvalue=True, offvalue=False)
option4 = ttk.Checkbutton(frame, text="Driver Information", variable=driverInfo, onvalue=True, offvalue=False)
option5 = ttk.Checkbutton(frame, text="Connected USB Devices", variable=usbDevices, onvalue=True, offvalue=False)

runButton = ttk.Button(frame, text="Start", command=runFunction)
infoButton = ttk.Button(frame, text="Help")

label1.grid(sticky=W, pady=(0, 5))
option1.grid(sticky=W)
option2.grid(sticky=W)
option3.grid(sticky=W)
option4.grid(sticky=W)
option5.grid(sticky=W)
runButton.grid(sticky=E, row=7, pady=(10, 0))
infoButton.grid(sticky=E, row=7, column=1, pady=(10, 0))
root.mainloop()