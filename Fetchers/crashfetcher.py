import shutil

from exceptions import fileDuplicate
from checks import *

def crash(directory):
    minidumpCheck()
    try:
        shutil.copytree(r"C:\Windows\Minidump", rf"{directory}\Minidumps")
    except FileExistsError:
        raise fileDuplicate

