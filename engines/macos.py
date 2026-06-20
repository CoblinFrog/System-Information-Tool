from engines.base import BaseEngine
import subprocess

def _run_cmd(args: list) -> dict:
    sorted_info = {}

    try:
        raw_output = subprocess.check_output(args, stderr=subprocess.DEVNULL).decode().strip()
    except subprocess.CalledProcessError, FileNotFoundError:
        raw_output = ""

    for line in raw_output.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            sorted_info[key.strip()] = val.strip()
    return sorted_info

class MacOS(BaseEngine):
    def __init__(self):
        print("macOS detected, macOS engine initialized.")

    def get_cpu_info(self) -> dict:
        cpu_info = _run_cmd(["sysctl", "hw", "machdep.cpu"])

        try:
            l1i = int(cpu_info.get("hw.l1icachesize")) // 1024
            l1d = int(cpu_info.get("hw.l1dcachesize")) // 1024
            l2 = int(cpu_info.get("hw.l2cachesize")) // 1024
        except ValueError, TypeError:
            l1i, l1d, l2 = 0, 0, 0

        return {
            "core_count": cpu_info.get("hw.physicalcpu"),
            "p_core_count" : cpu_info.get("hw.perflevel0.physicalcpu"),
            "e_core_count" : cpu_info.get("hw.perflevel1.physicalcpu"),
            "brand": cpu_info.get("machdep.cpu.brand_string"),
            "architecture": subprocess.check_output(["uname", "-m"], stderr=subprocess.DEVNULL).decode().strip(),
            "frequency" : cpu_info.get("hw.cpufrequency"),
            # Cache sizes below may be incorrect and inaccurate, need to sort which is which
            "l1_instruction_cache" : l1i,
            "l1_data_cache": l1d,
            "l2_cache" : l2
        }

    #This might break when multiple GPUs are connected and have to add support for display detection later.
    def get_graphics_info(self) -> dict:
        graphics_info = _run_cmd(["system_profiler", "SPDisplaysDataType"])

        return {
            "brand" : graphics_info.get("Chipset Model"),
            "manufacturer": graphics_info.get("Vendor"),
            "metal_support": graphics_info.get("Metal Support"),
        }

    def get_memory_info(self) -> dict:
        memory_info = _run_cmd(["system_profiler", "SPMemoryDataType"])

        return {
            "total_memory" : memory_info.get("Memory"),
            "memory_type" : memory_info.get("Type"),
            "memory_manufacturer" : memory_info.get("Manufacturer")
        }

    #Need to make sure this works on nonbattery macs like iMacs.
    def get_battery_info(self) -> dict:
        battery_info = _run_cmd(["system_profiler", "SPPowerDataType"])

        return {
            "current_cycle_count" : battery_info.get("Cycle Count"),
            "battery_health" : battery_info.get("Maximum Capacity"),
            "battery_condition": battery_info.get("Condition"),
        }

    #Need to figure out what counts as misc info and what can be its own thing.
    def get_misc_info(self) -> dict:
        model_info = _run_cmd(["system_profiler", "SPHardwareDataType"])
        os_info = _run_cmd(["sw_vers"])

        return {
            "model_identifier": model_info.get("Model Identifier"),
            "model_name": model_info.get("Model Name"),
            "model_number": model_info.get("Model Number"),
            "os_version": f"{os_info.get("ProductName")} {os_info.get("ProductVersion")}",
            "os_build": os_info.get("BuildVersion"),
        }

    #Add storage systems, need to be aware about multiple drives installed and filesystems.
    #Add WiFi, Ethernet, and Bluetooth stuff?
    #Logs?
    #Audio devices?
    #Check firmware and os versions.
    #Add usb and thunderbolt ports?