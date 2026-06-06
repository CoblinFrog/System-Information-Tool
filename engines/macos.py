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

    def get_gpu_info(self) -> dict:
        return {
            "brand" : subprocess.check_output("system_profiler SPDisplaysDataType | awk -F: '/Chipset Model/ {print $2}'", shell=True).decode().strip(),
        }

    def get_memory_info(self) -> dict:
        return {
            "total_memory": int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode().strip())//(1024 ** 3),
            "memory_type" : subprocess.check_output("system_profiler SPMemoryDataType | awk -F: '/Type/ {print $2}'", shell=True).decode().strip(),
            "memory_manufacturer" : subprocess.check_output("system_profiler SPMemoryDataType | awk -F: '/Manufacturer/ {print $2}'", shell=True).decode().strip()

        }

    def get_misc_info(self) -> dict:
        return {
            "model_identifier": "",
            "serial_number": ""
        }

    def get_battery_info(self) -> dict:
        return {
            "current_cycle_count" : subprocess.check_output("system_profiler SPPowerDataType | awk -F: '/Cycle Count/ {print $2}'", shell=True).decode().strip(),
            "battery_health" : subprocess.check_output("system_profiler SPPowerDataType | awk -F: '/Maximum Capacity/ {print $2}'", shell=True).decode().strip(),
        }
