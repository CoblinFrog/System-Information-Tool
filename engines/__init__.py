import platform

if platform.system() == "Windows":
    from engines.windows import Windows
    engine = Windows()
elif platform.system() == "Darwin":
    from engines.macos import MacOS
    engine = MacOS()
else:
    raise RuntimeError(f"Current OS {platform.system()} is not supported.")
