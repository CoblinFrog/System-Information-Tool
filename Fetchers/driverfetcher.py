import os
def drivers(directory):
    with open(os.path.join(directory, "Driver Information.txt"), "w") as file:
        file.write("Test")