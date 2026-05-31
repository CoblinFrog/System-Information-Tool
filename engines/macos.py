from engines.base import BaseEngine

import subprocess
import psutil

class MacOS(BaseEngine):
    print("macos detected")

    def get_cpu_info(self) -> dict:
        return {
            "core_count": psutil.cpu_count(),
            "brand": subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip(),
            "architecture": subprocess.check_output(["uname", "-m"]).decode().strip()
                }


