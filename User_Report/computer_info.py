from cpuinfo import get_cpu_info
import wmi
from psutil import virtual_memory
info = get_cpu_info()


#cpu
brand_name = info['brand_raw']
architecture = info['arch']


#cpu
puter = wmi.WMI()

for gpu in puter.Win32_VideoController():
    gpu_name = gpu.Caption
    gpu_driver = gpu.DriverVersion
    gpu_manu = gpu.AdapterCompatibility
    
#ram
memory = virtual_memory()
ram = memory.total
available = memory.available
used = memory.used


computer_info = f"""
CPU:
    Brand: {brand_name}
    Architecture: {architecture}

GPU:
    Name: {gpu_name}
    Driver Version: {gpu_driver}
    Manufacturer: {gpu_manu}

RAM:
    Total: {ram}
    Available: {available}
    Used: {used}
"""