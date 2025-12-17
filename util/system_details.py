import wmi
import psutil
import cpuinfo
import pythoncom

def _wmi():
    pythoncom.CoInitialize()
    return wmi.WMI()

def get_ram_capability():
    c = _wmi()

    arrays = c.Win32_PhysicalMemoryArray()
    slots = 0
    max_ram_gb = 0

    for arr in arrays:
        slots += int(arr.MemoryDevices or 0)
        max_ram_gb += int(arr.MaxCapacity or 0)

    pythoncom.CoUninitialize()
    return slots, round(max_ram_gb / (1024 ** 2), 2)


def get_ram_modules():
    c = _wmi()
    modules = []

    for mem in c.Win32_PhysicalMemory():
        modules.append({
            "Slot": mem.DeviceLocator,
            "Capacidade (GB)": round(int(mem.Capacity) / (1024**3), 2),
            "Velocidade (MHz)": mem.Speed,
            "Fabricante": mem.Manufacturer,
            "Tipo": mem.MemoryType,
            "Serial": mem.SerialNumber
        })

    pythoncom.CoUninitialize()
    return modules


def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    return {
        "Modelo": info.get("brand_raw"),
        "Arquitetura": info.get("arch"),
        "Bits": info.get("bits"),
        "Frequência Base": info.get("hz_advertised_friendly"),
        "Núcleos": info.get("count")
    }

def get_gpu_info():
    c = _wmi()
    gpus = []

    for gpu in c.Win32_VideoController():
        gpus.append({
            "Nome": gpu.Name,
            "VRAM (MB)": round(int(gpu.AdapterRAM or 0) / (1024**2), 2),
            "Driver": gpu.DriverVersion
        })

    pythoncom.CoUninitialize()
    return gpus


def get_disks():
    c = _wmi()
    disks = []

    for d in c.Win32_DiskDrive():
        disks.append({
            "Modelo": d.Model,
            "Interface": d.InterfaceType,
            "Tamanho (GB)": round(int(d.Size) / (1024**3), 2),
            "Serial": d.SerialNumber
        })

    pythoncom.CoUninitialize()
    return disks
