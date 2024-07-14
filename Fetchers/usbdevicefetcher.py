import os

def usb(directory):
    with open(os.path.join(directory, "USB Device Information.txt"), "w") as file:
        file.write("Test")