import os

def hardware(directory):
    with open(os.path.join(directory, "Hardware Information.txt"), "w") as file:
        file.write("Test")