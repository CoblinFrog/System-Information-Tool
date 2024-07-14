import platform
import os

from checks import *

def operatingsystem(directory):
   with open(os.path.join(directory, "Operating System Information.txt"), "w") as file:
       file.write(f"OS Name: Windows {platform.release()} \nWindows Version: {platform.version()} \nWindows Machine Type: {platform.machine()} \nWindows Architecture: {platform.architecture()[0]}")
       file.close()