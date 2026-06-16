from engines.base import BaseEngine

import subprocess

class MacOS(BaseEngine):
    def __init__(self):
        print("macOS detected, macOS engine initialized.")

    def _run_cmd(self, args: list ) -> str:
        try:
            return subprocess.check_output(args, stderr=subprocess.DEVNULL).decode().strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def get_cpu_info(self) -> dict:

        raw_info = self._run_cmd(["sysctl", "hw", "machdep.cpu"])
        cpu_info = {}
        for line in raw_info.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                cpu_info[key.strip()] = val.strip()

        def get_info(key, value="Unavailable"):
            return cpu_info.get(key, value)

        try:
            l1i = int(get_info("hw.l1icachesize", 0)) // 1024
            l1d = int(get_info("hw.l1dcachesize", 0)) // 1024
            l2 = int(get_info("hw.l2cachesize", 0)) // 1024
        except ValueError:
            l1i, l1d, l2 = 0, 0, 0

        #might wanna try different process, take entire entry, format and index it individually. might be more "secure" and optimized that way.
        return {
            "core_count": get_info("hw.physicalcpu"),
            "p_core_count" : get_info("hw.perflevel0.physicalcpu"),
            "e_core_count" : get_info("hw.perflevel1.physicalcpu"),
            "brand": get_info("machdep.cpu.brand_string"),
            "architecture": self._run_cmd(["uname", "-m"]),
            "frequency" : get_info("hw.cpufrequency"),
            # Cache sizes below may be incorrect and inaccurate, need to sort which is which
            "l1_instruction_cache" : l1i,
            "l1_data_cache": l1d,
            "l2_cache" : l2
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
            "model_identifier": subprocess.check_output("system_profiler SPHardwareDataType | awk -F: '/Model Identifier:/ {print $2}'", shell=True).decode().strip(),
            "serial_number": ""
        }

    def get_battery_info(self) -> dict:
        return {
            "current_cycle_count" : subprocess.check_output("system_profiler SPPowerDataType | awk -F: '/Cycle Count/ {print $2}'", shell=True).decode().strip(),
            "battery_health" : subprocess.check_output("system_profiler SPHardwareDataType | awk -F: '/Maximum Capacity/ {print $2}'", shell=True).decode().strip(),
        }
