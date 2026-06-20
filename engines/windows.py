from engines.base import BaseEngine

import subprocess

def _get_info(info: dict, key, value="Unavailable"):
        return dict.get(key, value)

def _run_cmd(args: list) -> str:
    try:
        return subprocess.check_output(args, stderr=subprocess.DEVNULL).decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""

class Windows(BaseEngine):
    def __init__(self):
        print("Windows detected, Windows engine initialized.")

    """
        def get_cpu_info(self) -> dict:
        raw_info = _run_cmd(["sysctl", "hw", "machdep.cpu"])
        cpu_info = {}
        for line in raw_info.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                cpu_info[key.strip()] = val.strip()
        try:
            l1i = int(_get_info(cpu_info, "hw.l1icachesize", 0)) // 1024
            l1d = int(_get_info(cpu_info, "hw.l1dcachesize", 0)) // 1024
            l2 = int(_get_info(cpu_info, "hw.l2cachesize", 0)) // 1024
        except ValueError:
            l1i, l1d, l2 = 0, 0, 0

        return {
            "core_count": _get_info(cpu_info,"hw.physicalcpu"),
            "p_core_count" : _get_info(cpu_info,"hw.perflevel0.physicalcpu"),
            "e_core_count" : _get_info(cpu_info,"hw.perflevel1.physicalcpu"),
            "brand": _get_info(cpu_info,"machdep.cpu.brand_string"),
            "architecture": _run_cmd(["uname", "-m"]),
            "frequency" : _get_info(cpu_info,"hw.cpufrequency"),
            # Cache sizes below may be incorrect and inaccurate, need to sort which is which
            "l1_instruction_cache" : l1i,
            "l1_data_cache": l1d,
            "l2_cache" : l2
        }

    #This might break when multiple GPUs are connected and have to add support for display detection later.
    def get_gpu_info(self) -> dict:
        raw_info = _run_cmd(["system_profiler", "SPDisplaysDataType"])
        gpu_info = {}
        for line in raw_info.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                gpu_info[key.strip()] = val.strip()

        return {
            "brand" : _get_info(gpu_info,"Chipset Model"),
            "manufacturer": _get_info(gpu_info, "Vendor"),
            "metal_support": _get_info(gpu_info, "Metal Support"),
        }

    def get_memory_info(self) -> dict:
        raw_info = ""
        memory_info = {}
        for line in raw_info.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                memory_info[key.strip()] = val.strip()

        return {
            "total_memory" : _get_info(memory_info,"Memory"),
            "memory_type" : _get_info(memory_info,"Type"),
            "memory_manufacturer" : _get_info(memory_info,"Manufacturer")
        }

    def get_misc_info(self) -> dict:
        raw_info = _run_cmd(["system_profiler", "SPHardwareDataType"])
        misc_info = {}
        for line in raw_info.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                misc_info[key.strip()] = val.strip()

        return {
            "model_identifier": _get_info(misc_info,"Model Identifier"),
            "model_name" : _get_info(misc_info,"Model Name"),
            "model_number": _get_info(misc_info,"Model Number")
        }

    #Need to make sure this works on nonbattery macs like iMacs.
    def get_battery_info(self) -> dict:
        raw_info = _run_cmd(["system_profiler", "SPPowerDataType"])
        battery_info = {}
        for line in raw_info.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                battery_info[key.strip()] = val.strip()

        return {
            "current_cycle_count" : _get_info(battery_info,"Cycle Count"),
            "battery_health" : _get_info(battery_info,"Maximum Capacity"),
            "battery_condition": _get_info(battery_info, "Condition"),
        }
    """

