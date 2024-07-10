import subprocess
import os
from tkinter import *
from tkinter import ttk
import shutil
import zipfile
from datetime import datetime

from exceptions import *

user = os.getlogin()

filename = f"{datetime.now().strftime('%m-%d-%Y %H')}"
print(filename)

#UI Elements
root = Tk()
root.resizable(False, False)
frame = ttk.Frame(root, padding=20)
frame.grid(column=0, row=0)

crashFiles = BooleanVar(root, False)
hardwareInfo = BooleanVar(root, False)
osInfo = BooleanVar(root, False)
driverInfo = BooleanVar(root, False)
usbDevices = BooleanVar(root, False)
nameFormat = StringVar(root, "default")

root.title("System Information Tool")


def miniDump():
    downloadsPath = "None"
    if os.path.exists(rf"C:\Users\{user}\Downloads"):
        downloadsPath = rf"C:\Users\{user}\Downloads"
    elif os.path.exists(rf"C:\Users\OneDrive\{user}\Downloads"):
        downloadsPath = rf"C:\Users\OneDrive\{user}\Downloads"
    else:
        raise downloadNotFound

    if os.path.exists(r"C:\Windows\Minidump"):
        pass
    else:
        raise noMiniDump

    try:
        shutil.copytree(r"C:\Windows\Minidump", rf"{downloadsPath}\test\Minidumps")
    except:
        raise fileDuplicate


def runFunction():
    print("hello")
    miniDump()


label1 = ttk.Label(frame, text="Please choose below what you would like to be packaged into the .zip file:")
label1.config(font=("TkDefaultFont", 11))
option1 = ttk.Checkbutton(frame, text="Minidump/Crash Files", variable=crashFiles, onvalue=True, offvalue=False)
option2 = ttk.Checkbutton(frame, text="Hardware Information", variable=hardwareInfo, onvalue=True, offvalue=False)
option3 = ttk.Checkbutton(frame, text="Windows Operating System Information", variable=osInfo, onvalue=True,
                          offvalue=False)
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
