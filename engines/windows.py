import json
import subprocess
from engines.base import BaseEngine


# Helper function tailored for Windows PowerShell CIM queries
def _run_pwsh(cim_class: str, namespace: str = "root\\cimv2", filter_query: str = None) -> list:
    """
    Executes a PowerShell CIM query, converts it to JSON, and ALWAYS returns a list.
    Supports optional WMI filtering.
    """
    filter_str = f" -Filter \"{filter_query}\"" if filter_query else ""
    cmd = f"@((Get-CimInstance -Namespace '{namespace}' -ClassName '{cim_class}'{filter_str})) | ConvertTo-Json -Compress"

    try:
        raw_output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", cmd],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        if not raw_output:
            return []

        parsed = json.loads(raw_output)
        if isinstance(parsed, dict):
            return [parsed]
        return parsed

    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return []


def _format_cache(kb_size: int) -> str:
    """Helper to format cache sizes into readable KB or MB."""
    if kb_size == 0:
        return "Unknown"
    elif kb_size < 1024:
        return f"{kb_size} KB"
    else:
        return f"{kb_size // 1024} MB"


class Windows(BaseEngine):
    def __init__(self):
        print("Windows detected, Windows engine initialized.")

    #Make helper function be able to change the clock speed to GHz
    def get_cpu_info(self) -> dict:
        cpu_data = _run_pwsh("Win32_Processor")
        cache_data = _run_pwsh("Win32_CacheMemory")

        if not cpu_data:
            return {"brand": "Unknown CPU", "core_count": 0}

        primary_cpu = cpu_data[0]
        total_cores = sum(cpu.get("NumberOfCores", 0) for cpu in cpu_data)
        total_threads = sum(cpu.get("NumberOfLogicalProcessors", 0) for cpu in cpu_data)

        arch_code = primary_cpu.get("Architecture")
        arch = "x86_64" if arch_code == 9 else "ARM64" if arch_code == 12 else "x86"

        # Sum up cache levels across all installed processors
        l1_kb = sum(c.get("InstalledSize", 0) for c in cache_data if c.get("Level") == 3)
        l2_kb = sum(c.get("InstalledSize", 0) for c in cache_data if c.get("Level") == 4)
        l3_kb = sum(c.get("InstalledSize", 0) for c in cache_data if c.get("Level") == 5)

        return {
            "core_count": total_cores,
            "thread_count": total_threads,
            "brand": primary_cpu.get("Name", "Unknown CPU"),
            "architecture": arch,
            "base_frequency": f"{primary_cpu.get('MaxClockSpeed', 0)/1000} GHz",
            "l1_cache": _format_cache(l1_kb),
            "l2_cache": _format_cache(l2_kb),
            "l3_cache": _format_cache(l3_kb)
        }

    def get_graphics_info(self) -> dict:
        gpu_data = _run_pwsh("Win32_VideoController")
        monitor_data = _run_pwsh("Win32_PnPEntity", filter_query="PNPClass='Monitor'")

        gpus = []
        displays = []

        # Get DirectX version safely
        try:
            dx_cmd = "(Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\DirectX' -Name 'Version' -ErrorAction SilentlyContinue).Version"
            dx_version = subprocess.check_output(["powershell", "-NoProfile", "-Command", dx_cmd],
                                                 stderr=subprocess.DEVNULL).decode().strip()
            if not dx_version: dx_version = "DirectX 12 (Default)"
        except:
            dx_version = "Unknown"

        # Hardware Subsystem Vendor Mapping dictionary
        # Covers major board manufacturers in the consumer ecosystem
        sub_vendor_map = {
            "1462": "MSI",
            "1043": "ASUS",
            "1458": "Gigabyte",
            "19DA": "Zotac",
            "3842": "EVGA",
            "107D": "Leadtek",
            "10B0": "Gainward",
            "1569": "Palit",
            "1682": "XFX",
            "1002": "AMD (Reference)",
            "10DE": "NVIDIA (Founders)",
            "8086": "Intel (Reference)",
            "17AA": "Lenovo",
            "1028": "Dell / Alienware",
            "103C": "HP"
        }

        for gpu in gpu_data:
            pnp_id = gpu.get("PNPDeviceID", "")

            if "PCI\\" not in pnp_id:
                continue

            vendor = "Unknown Vendor"
            try:
                import re
                subsys_match = re.search(r"SUBSYS_([0-9A-Fa-f]{4})([0-9A-Fa-f]{4})", pnp_id)
                if not subsys_match:
                    subsys_match = re.search(r"SUBSYS&[0-9A-Fa-f_]*&REV_[0-9A-Fa-f_]*", pnp_id)  # alternative formats

                # The secondary 4 digits of SUBSYS denote the actual layout manufacturer
                if subsys_match and len(subsys_match.groups()) >= 2:
                    subsys_vendor_id = subsys_match.group(2).upper()
                    vendor = sub_vendor_map.get(subsys_vendor_id, f"OEM (ID: {subsys_vendor_id})")
                else:
                    # Alternative backup parsing block if string formatting drops segments
                    chunks = pnp_id.split("&")
                    for chunk in chunks:
                        if chunk.startswith("SUBSYS_") and len(chunk) >= 15:
                            subsys_vendor_id = chunk[11:15].upper()
                            vendor = sub_vendor_map.get(subsys_vendor_id, f"OEM (ID: {subsys_vendor_id})")
                            break
            except:
                pass

            # Extract the raw Device & Vendor ID pattern to match with the 64-bit registry profile
            gpu_match_id = "&".join(pnp_id.split("&")[0:2]) if pnp_id else ""

            vram_str = "Unknown"
            if gpu_match_id:
                try:
                    reg_cmd = (
                        f"Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e968-e325-11ce-bfc1-08002be10318}}\\0*' "
                        f"-ErrorAction SilentlyContinue | "
                        f"Where-Object {{ $_.MatchingDeviceId -like '{gpu_match_id}*' }} | "
                        f"Select-Object -ExpandProperty HardwareInformation.qwMemorySize -First 1"
                    )

                    reg_out = subprocess.check_output(["powershell", "-NoProfile", "-Command", reg_cmd],
                                                      stderr=subprocess.DEVNULL).decode().strip()

                    if reg_out:
                        bytes_val = int(reg_out)
                        vram_str = f"{round(bytes_val // (1024 ** 3), 1)} GB"
                except:
                    vram_str = "Unknown"

            if vram_str == "Unknown":
                try:
                    vram_bytes = int(gpu.get("AdapterRAM", 0))
                    if vram_bytes >= 4293918720 or vram_bytes < 0:
                        vram_str = "4.0+ GB (Exceeds WMI limit)"
                    else:
                        vram_str = f"{round(vram_bytes // (1024 ** 3), 1)} GB"
                except (ValueError, TypeError):
                    vram_str = "Unknown"

            gpus.append({
                "name": gpu.get("Name", "Unknown GPU"),
                "chipset_manufacturer": gpu.get("AdapterCompatibility", "Unknown manufacturer"),
                "vendor": vendor,
                "directx_version": dx_version,
                "vram": vram_str,
            })

        for display in monitor_data:
            displays.append({
                "name": display.get("Name", "Generic Display"),
                "status": display.get("Status", "Unknown"),
            })

        return {"gpus": gpus, "displays": displays}

    #How would this function with multiple manufacturers and different sticks?
    def get_memory_info(self) -> dict:
        memory_modules = _run_pwsh("Win32_PhysicalMemory")

        if not memory_modules:
            return {"total_memory": "Unknown", "memory_type": "Unknown", "memory_manufacturer": "Unknown",
                    "speed": "Unknown"}

        total_capacity_bytes = sum(int(stick.get("Capacity", 0)) for stick in memory_modules)
        total_gb = total_capacity_bytes // (1024 ** 3)

        first_stick = memory_modules[0]

        # Fetch Memory Speed (ConfiguredClockSpeed represents the active running speed profile)
        speed_val = first_stick.get("ConfiguredClockSpeed") or first_stick.get("Speed", "Unknown")

        mem_type_code = first_stick.get("SMBIOSMemoryType", 0)
        type_mapping = {24: "DDR3", 26: "DDR4", 34: "DDR5"}

        return {
            "total_memory": f"{total_gb} GB",
            "speed": f"{speed_val} MT/s" if str(speed_val).isdigit() else "Unknown",
            "memory_type": type_mapping.get(mem_type_code, f"Type Code {mem_type_code}"),
            "memory_manufacturer": first_stick.get("Manufacturer", "Unknown"),
        }

    def get_battery_info(self) -> dict:
        battery_info = _run_pwsh("Win32_Battery")

        if not battery_info:
            return {
                "battery_health": "N/A",
                "battery_condition": "N/A"
            }

        primary_battery = battery_info[0]

        return {
            "battery_health": f"{primary_battery.get('EstimatedChargeRemaining', 'Unknown')}%",
            "battery_condition": primary_battery.get("Status", "Unknown")
        }

    def get_storage_info(self) -> dict:
        physical_disks = _run_pwsh("MSFT_PhysicalDisk", namespace="Root\\Microsoft\\Windows\\Storage")
        volumes_data = _run_pwsh("MSFT_Volume", namespace="Root\\Microsoft\\Windows\\Storage")

        drives = []
        volumes = []

        bus_types = {7: "USB", 11: "SATA", 17: "NVMe"}
        media_types = {3: "HDD", 4: "SSD"}

        # SMART HealthStatus translation map for MSFT_PhysicalDisk
        health_status_map = {
            0: "Healthy",
            1: "Warning / Degraded",
            2: "Unhealthy / Predictive Failure"
        }

        for disk in physical_disks:
            bus = disk.get("BusType", 0)

            # Extract raw health status and match it against our map
            raw_health = disk.get("HealthStatus", "Unknown")
            try:
                # Convert to integer in case it's stored as a string numeric
                clean_health = health_status_map.get(int(raw_health), "Unknown")
            except (ValueError, TypeError):
                clean_health = "Unknown"

            drives.append({
                "name": disk.get("FriendlyName", "Unknown Drive"),
                "detachable": "Yes" if bus == 7 else "No",
                "removable": "No",
                "drive_type": f"{media_types.get(disk.get('MediaType', 0), 'Unknown')} ({bus_types.get(bus, 'Unknown')})",
                "size": f"{int(disk.get('Size', 0)) // (1024 ** 3)} GB",
                "smart_status": clean_health  # Now outputs clean string tags
            })

        for vol in volumes_data:
            if not vol.get("Size"):
                continue

            letter = vol.get("DriveLetter")
            drive_letter = f"{letter}:\\" if letter else "Hidden Partition"

            volumes.append({
                "name": vol.get("FileSystemLabel") or "Local Disk",
                "drive_letter": drive_letter,
                "partition_type": vol.get("FileSystem", "Unknown"),
                "size": f"{int(vol.get('Size', 0)) // (1024 ** 3)} GB"
            })

        return {"drives": drives, "volumes": volumes}

    def get_os_info(self) -> dict:
        os_info = _run_pwsh("Win32_OperatingSystem")
        bios_info = _run_pwsh("Win32_BIOS")

        primary_os = os_info[0] if os_info else {}
        primary_bios = bios_info[0] if bios_info else {}

        # Fetch BIOS Mode (UEFI vs Legacy) via Get-ComputerInfo
        try:
            bios_cmd = "(Get-ComputerInfo -Property BiosFirmwareType).BiosFirmwareType"
            bios_mode = subprocess.check_output(["powershell", "-NoProfile", "-Command", bios_cmd],
                                                stderr=subprocess.DEVNULL).decode().strip()
            if not bios_mode: bios_mode = "Unknown"
        except:
            bios_mode = "Unknown"

        return {
            "os_version": primary_os.get("Caption", "Unknown OS"),
            "os_build": primary_os.get("BuildNumber", "Unknown Build"),
            "kernel_version": primary_os.get("Version", "Unknown Kernel"),
            "bios_version": primary_bios.get("SMBIOSBIOSVersion", "Unknown Firmware"),
            "bios_mode": bios_mode.upper(),
        }

    def get_model_info(self) -> dict:
        # Pull the primary computer specs and the underlying physical motherboard specs
        sys_data = _run_pwsh("Win32_ComputerSystem")
        board_data = _run_pwsh("Win32_BaseBoard")

        sys_info = sys_data[0] if sys_data else {}
        board_info = board_data[0] if board_data else {}

        sys_vendor = sys_info.get("Manufacturer", "Unknown")
        sys_model = sys_info.get("Model", "Unknown")

        board_vendor = board_info.get("Manufacturer", "Unknown")
        board_model = board_info.get("Product", "Unknown")

        is_custom_build = sys_model.strip().lower() == board_model.strip().lower()
        display_system_type = "Custom Desktop" if is_custom_build else "Pre-built / Laptop"

        return {
            "model_type": display_system_type,
            "model_brand": sys_vendor,
            "model_name": sys_model,
            "motherboard_manufacturer": board_vendor,
            "motherboard_model": board_model
        }