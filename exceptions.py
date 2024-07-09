import os.path
class downloadNotFound(Exception):
    def __init__(self, message="No downloads folder found"):
        self.message = message
        super().__init__(message)

class noMiniDump(Exception):
    def __init__(self, message="No Minidump folder was found"):
        self.message = message
        super().__init__(message)