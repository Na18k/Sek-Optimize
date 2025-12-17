import wmi
import psutil
import cpuinfo
import pythoncom
import sys
import win32event
import win32api
import winerror

# ---------- Bloqueio de instância única ----------
mutex = win32event.CreateMutex(None, False, "SekOptimizeMutex")
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    sys.exit(0)  # Sai imediatamente se outra instância estiver rodando

# ---------- Inicialização COM única ----------
pythoncom.CoInitialize()

# ---------- Função auxiliar WMI ----------
def _wmi():
    return wmi.WMI()  # COM já inicializado globalmente

# ---------- RAM ----------
def get_ram_capability():
    c = wmi.WMI()
    arrays = c.Win32_PhysicalMemoryArray()
    slots = 0
    max_ram_gb = 0
    for arr in arrays:
        slots += int(arr.MemoryDevices or 0)
        max_ram_gb += int(arr.MaxCapacity or 0)
    max_ram_gb = round(max_ram_gb / (1024 ** 2), 2)
    return slots, max_ram_gb

def get_ram_modules():
    c = wmi.WMI()
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
    return modules

# ---------- CPU ----------
def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    return {
        "Modelo": info.get("brand_raw"),
        "Arquitetura": info.get("arch"),
        "Bits": info.get("bits"),
        "Frequência Base": info.get("hz_advertised_friendly"),
        "Núcleos": info.get("count")
    }

# ---------- GPU ----------
def get_gpu_info():
    c = wmi.WMI()
    gpus = []
    for gpu in c.Win32_VideoController():
        gpus.append({
            "Nome": gpu.Name,
            "VRAM (MB)": round(int(gpu.AdapterRAM or 0) / (1024**2), 2),
            "Driver": gpu.DriverVersion
        })
    return gpus

# ---------- Discos ----------
def get_disks():
    c = wmi.WMI()
    disks = []
    for d in c.Win32_DiskDrive():
        disks.append({
            "Modelo": d.Model,
            "Interface": d.InterfaceType,
            "Tamanho (GB)": round(int(d.Size) / (1024**3), 2),
            "Serial": d.SerialNumber
        })
    return disks

# ---------- Finalização COM ----------
def finalize():
    pythoncom.CoUninitialize()

# ---------- Exemplo de uso interno ----------
if __name__ == "__main__":
    # Aqui você chamaria suas funções internamente
    # Exemplo:
    ram_slots, ram_max = get_ram_capability()
    ram_modules = get_ram_modules()
    cpu = get_cpu_info()
    gpu = get_gpu_info()
    disks = get_disks()

    # Finaliza COM ao terminar
    finalize()
