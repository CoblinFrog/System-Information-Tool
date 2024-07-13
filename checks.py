import platform
import os

from exceptions import *

user = os.getlogin()



def check():
    print("Checking operating system")
    if not platform.system() == "Windows":
        raise notWindows

def downloadsCheck():
    print("Checking for Downloads folder")
    downloadsPath = "None"
    if os.path.exists(rf"C:\Users\{user}\Downloads"):
        downloadsPath = rf"C:\Users\{user}\Downloads"
        print("Downloads folder found")
    elif os.path.exists(rf"C:\Users\OneDrive\{user}\Downloads"):
        downloadsPath = rf"C:\Users\OneDrive\{user}\Downloads"
        print("Downloads folder found")
    else:
        raise downloadNotFound
    return downloadsPath

def minidumpCheck():
    print("Checking for Minidumps folder")
    if os.path.exists(r"C:\Windows\Minidump"):
        print("Minidump folder found")
        pass
    else:
        raise noMiniDump

def optionsChecker(crashFiles, hardwareInfo, osInfo, driverInfo, usbDevices):
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
        return True
    else:
        return False


