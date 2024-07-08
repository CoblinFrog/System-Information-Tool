import subprocess
import os
from tkinter import *
from tkinter import ttk

#UI Elements
root = Tk()
frame = ttk.Frame(root, padding=5)
frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

crashFiles = BooleanVar(root, False)
hardwareInfo = BooleanVar(root, False)
osInfo = BooleanVar(root, False)
driverInfo = BooleanVar(root, False)
usbDevices = BooleanVar(root, False)

root.geometry("600x400")
root.title("System Information Tool")

label1 = ttk.Label(root, text="Please choose below what you would like to be packaged into the .zip file:")
option1 = ttk.Checkbutton(root, text="Minidump/Crash Files", variable=crashFiles, onvalue=True, offvalue=False)
option2 = ttk.Checkbutton(root, text="Hardware Information", variable=hardwareInfo, onvalue=True, offvalue=False)
option3 = ttk.Checkbutton(root, text="Windows Operating System Information", variable=osInfo, onvalue=True, offvalue=False)
option4 = ttk.Checkbutton(root, text="Driver Information", variable=driverInfo, onvalue=True, offvalue=False)
option5 = ttk.Checkbutton(root, text="Connected USB Devices", variable=usbDevices, onvalue=True, offvalue=False)

root.mainloop()