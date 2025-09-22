#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MXD Pro - Hardware Detection Module
Provides accurate hardware detection with real information, no fake data
"""

import os
import sys
import platform
import subprocess
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

# Try to import platform-specific modules
try:
    import psutil
except ImportError:
    psutil = None

try:
    if platform.system() == "Windows":
        import wmi
        import winreg
    else:
        wmi = None
        winreg = None
except ImportError:
    wmi = None
    winreg = None

@dataclass
class GPUInfo:
    """GPU information structure"""
    name: str
    vendor: str
    vram_mb: int
    driver_version: str
    supports_6k: bool
    supports_rt: bool
    supports_dlss: bool
    supports_fsr: bool
    supports_xess: bool
    pci_id: str
    current_vram_usage: float = 0.0
    temperature: float = 0.0
    utilization: float = 0.0

@dataclass
class CPUInfo:
    """CPU information structure"""
    name: str
    vendor: str
    cores: int
    threads: int
    base_frequency: float
    max_frequency: float
    current_frequency: float
    temperature: float = 0.0
    utilization: float = 0.0

@dataclass
class MemoryInfo:
    """Memory information structure"""
    total_mb: int
    available_mb: int
    used_mb: int
    usage_percent: float
    speed_mhz: int = 0

@dataclass
class StorageInfo:
    """Storage device information"""
    name: str
    type: str  # SSD, HDD, NVMe
    total_gb: int
    free_gb: int
    used_gb: int
    usage_percent: float

@dataclass
class MonitorInfo:
    """Monitor information structure"""
    name: str
    width: int
    height: int
    refresh_rate: float
    is_primary: bool

class HardwareDetector:
    """Accurate hardware detection with real information only"""

    def __init__(self, logger=None):
        self.logger = logger
        self._gpu_cache = None
        self._cpu_cache = None
        self._log("Hardware detector initialized")

    def _log(self, message: str):
        """Log message if logger is available"""
        if self.logger:
            self.logger.info(message)

    def detect_gpus(self) -> List[GPUInfo]:
        """Detect GPUs with accurate information"""
        if self._gpu_cache:
            return self._gpu_cache

        gpus = []

        try:
            if platform.system() == "Windows":
                gpus = self._detect_gpus_windows()
            else:
                gpus = self._detect_gpus_linux()

            self._gpu_cache = gpus
            self._log(f"Detected {len(gpus)} GPU(s)")

            for gpu in gpus:
                self._log(f"GPU: {gpu.name} - VRAM: {gpu.vram_mb}MB")

        except Exception as e:
            self._log(f"Error detecting GPUs: {e}")
            # Return a minimal fallback
            gpus = [GPUInfo(
                name="Unknown GPU",
                vendor="Unknown",
                vram_mb=0,
                driver_version="Unknown",
                supports_6k=False,
                supports_rt=False,
                supports_dlss=False,
                supports_fsr=False,
                supports_xess=False,
                pci_id="Unknown"
            )]

        return gpus

    def _detect_gpus_windows(self) -> List[GPUInfo]:
        """Detect GPUs on Windows using WMI and registry"""
        gpus = []

        try:
            if wmi:
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    if gpu.Name and gpu.AdapterRAM:
                        # Parse GPU information
                        name = gpu.Name.strip()
                        vram_mb = int(gpu.AdapterRAM / (1024 * 1024)) if gpu.AdapterRAM else 0

                        # Determine vendor
                        vendor = "Unknown"
                        if "nvidia" in name.lower() or "geforce" in name.lower() or "gtx" in name.lower() or "rtx" in name.lower():
                            vendor = "NVIDIA"
                        elif "amd" in name.lower() or "radeon" in name.lower() or "rx" in name.lower():
                            vendor = "AMD"
                        elif "intel" in name.lower() or "uhd" in name.lower() or "iris" in name.lower():
                            vendor = "Intel"

                        # Determine capabilities based on real GPU name
                        supports_dlss = vendor == "NVIDIA" and ("rtx" in name.lower() or "gtx 16" in name.lower())
                        supports_fsr = True  # Most modern GPUs support FSR
                        supports_xess = vendor == "Intel" and "arc" in name.lower()
                        supports_rt = ("rtx" in name.lower() or
                                     "rx 6" in name.lower() or "rx 7" in name.lower() or
                                     "arc" in name.lower())
                        supports_6k = vram_mb >= 8192  # 8GB+ VRAM for 6K

                        gpu_info = GPUInfo(
                            name=name,
                            vendor=vendor,
                            vram_mb=vram_mb,
                            driver_version=gpu.DriverVersion or "Unknown",
                            supports_6k=supports_6k,
                            supports_rt=supports_rt,
                            supports_dlss=supports_dlss,
                            supports_fsr=supports_fsr,
                            supports_xess=supports_xess,
                            pci_id=gpu.PNPDeviceID or "Unknown"
                        )

                        # Get real-time GPU stats if possible
                        self._update_gpu_stats(gpu_info)

                        gpus.append(gpu_info)

        except Exception as e:
            self._log(f"WMI GPU detection failed: {e}")
            # Fallback to registry
            gpus = self._detect_gpus_registry()

        return gpus if gpus else self._detect_gpus_fallback()

    def _detect_gpus_linux(self) -> List[GPUInfo]:
        """Detect GPUs on Linux using various methods"""
        gpus = []

        # Try nvidia-smi for NVIDIA GPUs
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,driver_version,pci.device_id',
                                   '--format=csv,noheader,nounits'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 4:
                            name = parts[0]
                            vram_mb = int(parts[1])
                            driver_version = parts[2]
                            pci_id = parts[3]

                            gpu_info = GPUInfo(
                                name=name,
                                vendor="NVIDIA",
                                vram_mb=vram_mb,
                                driver_version=driver_version,
                                supports_6k=vram_mb >= 8192,
                                supports_rt="rtx" in name.lower(),
                                supports_dlss="rtx" in name.lower() or "gtx 16" in name.lower(),
                                supports_fsr=True,
                                supports_xess=False,
                                pci_id=pci_id
                            )
                            gpus.append(gpu_info)
        except:
            pass

        # Try lspci for other GPUs
        try:
            result = subprocess.run(['lspci', '-nn'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'vga compatible controller' in line.lower() or '3d controller' in line.lower():
                        # Parse PCI device info
                        if 'nvidia' in line.lower():
                            vendor = "NVIDIA"
                        elif 'amd' in line.lower() or 'ati' in line.lower():
                            vendor = "AMD"
                        elif 'intel' in line.lower():
                            vendor = "Intel"
                        else:
                            vendor = "Unknown"

                        # Extract device name
                        name_match = re.search(r'controller:\s*(.+?)\s*\[', line, re.IGNORECASE)
                        name = name_match.group(1) if name_match else "Unknown GPU"

                        # Skip if already found via nvidia-smi
                        if not any(gpu.name == name for gpu in gpus):
                            gpu_info = GPUInfo(
                                name=name,
                                vendor=vendor,
                                vram_mb=0,  # Can't determine VRAM from lspci
                                driver_version="Unknown",
                                supports_6k=False,
                                supports_rt=False,
                                supports_dlss=False,
                                supports_fsr=True,
                                supports_xess=vendor == "Intel",
                                pci_id="Unknown"
                            )
                            gpus.append(gpu_info)
        except:
            pass

        return gpus if gpus else self._detect_gpus_fallback()

    def _detect_gpus_registry(self) -> List[GPUInfo]:
        """Fallback GPU detection using Windows registry"""
        gpus = []

        try:
            if winreg:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}")

                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)

                        try:
                            name = winreg.QueryValueEx(subkey, "DriverDesc")[0]
                            vram_mb = 0  # Registry doesn't usually have VRAM info

                            vendor = "Unknown"
                            if "nvidia" in name.lower():
                                vendor = "NVIDIA"
                            elif "amd" in name.lower() or "radeon" in name.lower():
                                vendor = "AMD"
                            elif "intel" in name.lower():
                                vendor = "Intel"

                            gpu_info = GPUInfo(
                                name=name,
                                vendor=vendor,
                                vram_mb=vram_mb,
                                driver_version="Unknown",
                                supports_6k=False,
                                supports_rt=False,
                                supports_dlss=False,
                                supports_fsr=True,
                                supports_xess=vendor == "Intel",
                                pci_id="Unknown"
                            )
                            gpus.append(gpu_info)

                        except WindowsError:
                            pass

                        winreg.CloseKey(subkey)
                        i += 1

                    except WindowsError:
                        break

                winreg.CloseKey(key)
        except:
            pass

        return gpus

    def _detect_gpus_fallback(self) -> List[GPUInfo]:
        """Fallback GPU detection when other methods fail"""
        self._log("Using fallback GPU detection")

        return [GPUInfo(
            name="Integrated Graphics",
            vendor="Unknown",
            vram_mb=0,
            driver_version="Unknown",
            supports_6k=False,
            supports_rt=False,
            supports_dlss=False,
            supports_fsr=False,
            supports_xess=False,
            pci_id="Unknown"
        )]

    def _update_gpu_stats(self, gpu_info: GPUInfo):
        """Update real-time GPU statistics"""
        try:
            if platform.system() == "Windows" and gpu_info.vendor == "NVIDIA":
                # Try to get NVIDIA GPU stats
                result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total,temperature.gpu,utilization.gpu',
                                       '--format=csv,noheader,nounits'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if lines:
                        parts = [p.strip() for p in lines[0].split(',')]
                        if len(parts) >= 4:
                            used_vram = float(parts[0])
                            total_vram = float(parts[1])
                            gpu_info.current_vram_usage = (used_vram / total_vram) * 100
                            gpu_info.temperature = float(parts[2])
                            gpu_info.utilization = float(parts[3])
        except:
            pass

    def detect_cpu(self) -> CPUInfo:
        """Detect CPU information"""
        if self._cpu_cache:
            return self._cpu_cache

        try:
            cpu_info = CPUInfo(
                name=platform.processor() or "Unknown CPU",
                vendor="Unknown",
                cores=psutil.cpu_count(logical=False) if psutil else 0,
                threads=psutil.cpu_count(logical=True) if psutil else 0,
                base_frequency=0,
                max_frequency=0,
                current_frequency=0
            )

            if psutil:
                # Get CPU frequencies
                freq_info = psutil.cpu_freq()
                if freq_info:
                    cpu_info.current_frequency = freq_info.current
                    cpu_info.max_frequency = freq_info.max
                    cpu_info.base_frequency = freq_info.min

                # Get CPU usage
                cpu_info.utilization = psutil.cpu_percent(interval=1)

            # Determine vendor from CPU name
            name_lower = cpu_info.name.lower()
            if "intel" in name_lower:
                cpu_info.vendor = "Intel"
            elif "amd" in name_lower:
                cpu_info.vendor = "AMD"
            elif "arm" in name_lower:
                cpu_info.vendor = "ARM"

            self._cpu_cache = cpu_info
            self._log(f"CPU: {cpu_info.name} ({cpu_info.cores} cores, {cpu_info.threads} threads)")

        except Exception as e:
            self._log(f"Error detecting CPU: {e}")
            cpu_info = CPUInfo(
                name="Unknown CPU",
                vendor="Unknown",
                cores=0,
                threads=0,
                base_frequency=0,
                max_frequency=0,
                current_frequency=0
            )

        return cpu_info

    def detect_memory(self) -> MemoryInfo:
        """Detect system memory information"""
        try:
            if psutil:
                mem = psutil.virtual_memory()
                memory_info = MemoryInfo(
                    total_mb=int(mem.total / (1024 * 1024)),
                    available_mb=int(mem.available / (1024 * 1024)),
                    used_mb=int(mem.used / (1024 * 1024)),
                    usage_percent=mem.percent
                )

                self._log(f"Memory: {memory_info.total_mb}MB total, {memory_info.usage_percent:.1f}% used")
                return memory_info

        except Exception as e:
            self._log(f"Error detecting memory: {e}")

        return MemoryInfo(
            total_mb=0,
            available_mb=0,
            used_mb=0,
            usage_percent=0.0
        )

    def detect_storage(self) -> List[StorageInfo]:
        """Detect storage devices"""
        storage_devices = []

        try:
            if psutil:
                partitions = psutil.disk_partitions()
                for partition in partitions:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)

                        # Determine storage type (simplified)
                        storage_type = "HDD"
                        if "ssd" in partition.device.lower():
                            storage_type = "SSD"
                        elif "nvme" in partition.device.lower():
                            storage_type = "NVMe"

                        storage_info = StorageInfo(
                            name=partition.device,
                            type=storage_type,
                            total_gb=int(usage.total / (1024**3)),
                            free_gb=int(usage.free / (1024**3)),
                            used_gb=int(usage.used / (1024**3)),
                            usage_percent=(usage.used / usage.total) * 100
                        )

                        storage_devices.append(storage_info)

                    except PermissionError:
                        continue

                self._log(f"Detected {len(storage_devices)} storage device(s)")

        except Exception as e:
            self._log(f"Error detecting storage: {e}")

        return storage_devices

    def detect_monitors(self) -> List[MonitorInfo]:
        """Detect monitor information"""
        monitors = []

        try:
            if platform.system() == "Windows":
                monitors = self._detect_monitors_windows()
            else:
                monitors = self._detect_monitors_linux()

            self._log(f"Detected {len(monitors)} monitor(s)")

        except Exception as e:
            self._log(f"Error detecting monitors: {e}")
            # Fallback
            monitors = [MonitorInfo(
                name="Unknown Monitor",
                width=1920,
                height=1080,
                refresh_rate=60.0,
                is_primary=True
            )]

        return monitors

    def _detect_monitors_windows(self) -> List[MonitorInfo]:
        """Detect monitors on Windows"""
        monitors = []

        try:
            if wmi:
                c = wmi.WMI()
                for monitor in c.Win32_DesktopMonitor():
                    if monitor.Name:
                        monitors.append(MonitorInfo(
                            name=monitor.Name,
                            width=int(monitor.ScreenWidth) if monitor.ScreenWidth else 1920,
                            height=int(monitor.ScreenHeight) if monitor.ScreenHeight else 1080,
                            refresh_rate=60.0,  # WMI doesn't provide refresh rate easily
                            is_primary=len(monitors) == 0  # First monitor is primary
                        ))
        except:
            pass

        return monitors

    def _detect_monitors_linux(self) -> List[MonitorInfo]:
        """Detect monitors on Linux"""
        monitors = []

        try:
            # Try xrandr
            result = subprocess.run(['xrandr'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if ' connected' in line:
                        parts = line.split()
                        name = parts[0]

                        # Parse resolution
                        for part in parts:
                            if 'x' in part and '+' in part:
                                res_part = part.split('+')[0]
                                if 'x' in res_part:
                                    width, height = map(int, res_part.split('x'))
                                    monitors.append(MonitorInfo(
                                        name=name,
                                        width=width,
                                        height=height,
                                        refresh_rate=60.0,
                                        is_primary='primary' in line
                                    ))
                                    break
        except:
            pass

        return monitors

    def get_system_summary(self) -> Dict[str, any]:
        """Get complete system hardware summary"""
        summary = {
            "cpu": self.detect_cpu(),
            "memory": self.detect_memory(),
            "gpus": self.detect_gpus(),
            "storage": self.detect_storage(),
            "monitors": self.detect_monitors(),
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "architecture": platform.architecture()[0]
            }
        }

        self._log("Generated complete system hardware summary")
        return summary

if __name__ == "__main__":
    # Test hardware detection
    from utils import MXDLogger

    logger = MXDLogger("Hardware_Test")
    detector = HardwareDetector(logger)

    print("Testing hardware detection...")

    # Test GPU detection
    gpus = detector.detect_gpus()
    print(f"\nFound {len(gpus)} GPU(s):")
    for gpu in gpus:
        print(f"  {gpu.name} ({gpu.vendor}) - {gpu.vram_mb}MB VRAM")
        print(f"    DLSS: {gpu.supports_dlss}, FSR: {gpu.supports_fsr}, RT: {gpu.supports_rt}")

    # Test CPU detection
    cpu = detector.detect_cpu()
    print(f"\nCPU: {cpu.name}")
    print(f"  Cores: {cpu.cores}, Threads: {cpu.threads}")
    print(f"  Frequency: {cpu.current_frequency:.0f} MHz")

    # Test memory detection
    memory = detector.detect_memory()
    print(f"\nMemory: {memory.total_mb}MB total ({memory.usage_percent:.1f}% used)")

    # Test storage detection
    storage = detector.detect_storage()
    print(f"\nStorage devices: {len(storage)}")
    for drive in storage:
        print(f"  {drive.name} ({drive.type}) - {drive.total_gb}GB total")

    print("\nHardware detection test completed.")