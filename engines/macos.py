import json

from engines.base import BaseEngine
import subprocess

#Add proper exception handling, fix unknown stuff.
def _run_cmd(args: list, j: bool = False) -> dict:
    if j:
        try:
            args = args + ["-json"]
            raw_output = subprocess.check_output(args, stderr=subprocess.DEVNULL).decode().strip()
            return json.loads(raw_output)
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return {}
    else:
        sorted_info = {}

        try:
            raw_output = subprocess.check_output(args, stderr=subprocess.DEVNULL).decode().strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
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

        return {
            "core_count": cpu_info.get("hw.physicalcpu"),
            "p_core_count" : cpu_info.get("hw.perflevel0.physicalcpu"),
            "e_core_count" : cpu_info.get("hw.perflevel1.physicalcpu"),
            "brand": cpu_info.get("machdep.cpu.brand_string"),
            "architecture": subprocess.check_output(["uname", "-m"], stderr=subprocess.DEVNULL).decode().strip(),
            "frequency" : cpu_info.get("hw.cpufrequency"),
            # Cache sizes below may be incorrect and inaccurate, need to sort which is which
            "l1_instruction_cache" : self.format_size_units(cpu_info.get("hw.l1icachesize")),
            "l1_data_cache": self.format_size_units(cpu_info.get("hw.l1dcachesize")),
            "l2_cache" : self.format_size_units(cpu_info.get("hw.l2cachesize"))
        }

    def get_graphics_info(self) -> dict:
        graphics_info = _run_cmd(["system_profiler", "SPDisplaysDataType"], True).get("SPDisplaysDataType", [])
        gpus = []
        displays = []
        metal_versions = {
            "spdisplays_metal1": "Metal 1",
            "spdisplays_metal2": "Metal 2",
            "spdisplays_metal3": "Metal 3",
            "spdisplays_metal4": "Metal 4",
            "spdisplays_metal5": "Metal 5",
        }
        main_display_values = {
            "spdisplays_yes": "Yes",
            "spdisplays_no": "No",
        }

        for gpu in graphics_info:
            metal_output = gpu.get("spdisplays_mtlgpufamilysupport", "")
            metal = metal_versions.get(
                metal_output, metal_output or "Metal Unsupported"
            )
            gpus.append(
                {
                    "name": gpu.get("_name", "Unknown"),
                    "manufacturer": gpu.get("spdisplays_vendor", "Unknown manufacturer")[13:],
                    "metal_support": metal,
                    "vram": gpu.get("spdisplays_vram", "Unknown"),
                }
            )

            connected_displays = gpu.get("spdisplays_ndrvs", [])
            for display in connected_displays:
                main_display_output = display.get("spdisplays_main", "Unknown")
                main_display = main_display_values.get(
                    main_display_output, main_display_output or "Metal Unsupported"
                )
                displays.append(
                    {
                        "name": display.get("_name", "Unknown"),
                        "display_type" : display.get("spdisplays_display_type", "Unknown")[11:],
                        "resolution" : display.get("_spdisplays_pixels", "Unknown resolution"),
                        "is_main_display" : main_display,
                    }
                )

        return {"gpus": gpus, "displays": displays}

    #This could break on macs with multiple memory modules, need to find what the output would be like.
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
            "current_cycle_count" : battery_info.get("Cycle Count", "Unknown cycle count"),
            "battery_health" : battery_info.get("Maximum Capacity", "Unknown capacity"),
            "battery_condition": battery_info.get("Condition", "Unknown condition"),
        }

    def get_storage_info(self) -> dict:
        target_datatypes = ["SPNVMeDataType", "SPSATADataType"]
        drives = []
        volumes = []

        for datatype in target_datatypes:
            raw_payload = _run_cmd(["system_profiler", datatype], True)
            if not raw_payload:
                continue

            info_list = raw_payload.get(datatype, [])

            for controller_entry in info_list:
                items = controller_entry.get("_items", [])

                for drive in items:
                    drive_type = "NVMe" if datatype == "SPNVMeDataType" else "SATA"

                    drives.append(
                        {
                            "name": drive.get("_name", "Unknown"),
                            "partition_map_type": drive.get("partition_map_type", "Unknown").replace("_", " ").title(),
                            "drive_type": drive_type,
                            "size": drive.get("size", "Unknown"),
                            "smart_status": drive.get("smart_status", "N/A").capitalize(),
                        }
                    )

                    drive_volumes = drive.get("volumes", [])
                    for volume in drive_volumes:
                        volumes.append(
                            {
                                "name": volume.get("_name", "Unknown"),
                                "bsd_name": volume.get("bsd_name", "Unknown"),
                                "partition_type": volume.get("iocontent", "Unknown").replace("_", " "),
                                "size": volume.get("size", "Unknown"),
                            }
                        )

        return {"drives": drives, "volumes": volumes}

    def get_os_info(self) -> dict:
        os_info = _run_cmd(["sw_vers"])
        firmware_info = _run_cmd(["system_profiler", "SPHardwareDataType"])

        return {
            "os_version": f"{os_info.get("ProductName")} {os_info.get("ProductVersion")}",
            "os_build": os_info.get("BuildVersion"),
            "kernel_version": subprocess.check_output(["uname", "-r"], stderr=subprocess.DEVNULL).decode().strip(),
            "system_firmware_version": firmware_info.get("System Firmware Version"),
            "os_loader_version": firmware_info.get("OS Loader Version"),
        }

    def get_model_info(self) -> dict:
        model_info = _run_cmd(["system_profiler", "SPHardwareDataType"])

        return {
            "model_identifier": model_info.get("Model Identifier"),
            "model_name": model_info.get("Model Name"),
            "model_number": model_info.get("Model Number"),
            "serial_number" : model_info.get("Serial Number (system)"),
        }

    #Add WiFi, Ethernet, and Bluetooth stuff?
    #Audio devices?
    #Add usb and thunderbolt ports?