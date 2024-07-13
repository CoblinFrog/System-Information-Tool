import shutil

from exceptions import *
from checks import *

def crash(filename):
    minidumpCheck()
    try:
        shutil.copytree(r"C:\Windows\Minidump", rf"{downloadsCheck()}\{filename}\Minidumps")
    except FileExistsError:
        raise fileDuplicate
