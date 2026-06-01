from engines.base import BaseEngine

import subprocess

class MacOS(BaseEngine):
    print("macos detected")

    def get_cpu_info(self) -> dict:
        frequency = subprocess.check_output(["sysctl", "-n", "hw.cpufrequency"]).decode().strip()
        if frequency == "":
            frequency = "Unavailable"

        return {
            "core_count": f"{subprocess.check_output(["sysctl", "-n", "hw.physicalcpu"]).decode().strip()} ({subprocess.check_output(["sysctl", "-n", "hw.perflevel0.physicalcpu"]).decode().strip()} Performance, {subprocess.check_output(["sysctl", "-n", "hw.perflevel1.physicalcpu"]).decode().strip()} Efficiency)",
            "brand": subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip(),
            "architecture": subprocess.check_output(["uname", "-m"]).decode().strip(),
            "frequency" : frequency,
            # Cache sizes below may be incorrect and inaccurate, need to sort which is which
            "l1_instruction_cache" : int(subprocess.check_output(["sysctl", "-n", "hw.l1icachesize"]).decode().strip())//1024,
            "l1_data_cache": int(subprocess.check_output(["sysctl", "-n", "hw.l1dcachesize"]).decode().strip())//1024,
            "l1_total_cache" : (int(subprocess.check_output(["sysctl", "-n", "hw.l1icachesize"]).decode().strip()) + int(subprocess.check_output(["sysctl", "-n", "hw.l1dcachesize"]).decode().strip()))//1024,
            "l2_cache" : int(subprocess.check_output(["sysctl", "-n", "hw.l2cachesize"]).decode().strip())//1024
        }

    def get_memory_info(self) -> dict:
        return {
            "memory_total": int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode().strip())//(1024 ** 3),
        }


