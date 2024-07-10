import os.path
class downloadNotFound(Exception):
    def __init__(self, message="No downloads folder found"):
        self.message = message
        super().__init__(message)

class noMiniDump(Exception):
    def __init__(self, message="No Minidump folder was found"):
        self.message = message
        super().__init__(message)

class fileDuplicate(Exception):
    def __init__(self, message="A file by that name is already created"):
        self.message = message
        super().__init__(message)

class noneSelected(Exception):
    def __init__(self, message="Please select at least one option"):
        self.message = message
        super().__init__(message)

