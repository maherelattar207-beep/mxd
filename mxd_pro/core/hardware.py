import platform
import subprocess
import re
import logging
from typing import List, Dict, Any

try:
    import psutil
except ImportError:
    psutil = None
    logging.error("psutil library not found. Hardware detection will be limited.")

try:
    if platform.system() == "Windows":
        import wmi
    else:
        wmi = None
except ImportError:
    wmi = None
    logging.warning("wmi library not found. GPU detection on Windows will be limited.")

class HardwareDetector:
    """Detects and provides detailed information about system hardware."""
    def __init__(self, logger):
        self.logger = logger

    def get_system_summary(self) -> Dict[str, Any]:
        """Returns a comprehensive dictionary of all detected hardware."""
        return {
            "cpu": self._detect_cpu(),
            "gpus": self._detect_gpus(),
            "memory": self._detect_memory(),
            "os": self._detect_os(),
        }

    def _detect_cpu(self) -> Dict[str, Any]:
        """Detects CPU information."""
        if not psutil: return {}
        try:
            return {
                "name": platform.processor() or "N/A",
                "cores": psutil.cpu_count(logical=False),
                "threads": psutil.cpu_count(logical=True),
                "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else 0,
            }
        except Exception as e:
            self.logger.error(f"Error detecting CPU: {e}")
            return {}

    def _detect_gpus(self) -> List[Dict[str, Any]]:
        """Detects GPU information, preferring WMI on Windows."""
        gpus = []
        if wmi:
            try:
                for gpu in wmi.WMI().Win32_VideoController():
                    gpu_info = {
                        "name": gpu.Name.strip(),
                        "vendor": self._get_vendor_from_name(gpu.Name),
                        "vram_mb": int(gpu.AdapterRAM / (1024*1024)) if gpu.AdapterRAM else 0,
                        "driver_version": gpu.DriverVersion,
                    }
                    gpus.append(gpu_info)
            except Exception as e:
                self.logger.error(f"WMI GPU detection failed: {e}")

        if not gpus:
            gpus.append({"name": "Generic Display Adapter", "vendor": "Unknown", "vram_mb": 0, "driver_version": "N/A"})

        # Add capabilities based on name
        for gpu in gpus:
            name_lower = gpu['name'].lower()
            gpu['supports_dlss'] = "rtx" in name_lower
            gpu['supports_fsr'] = True  # Generally available
            gpu['supports_xess'] = "arc" in name_lower
            gpu['supports_rt'] = "rtx" in name_lower or ("rx 6" in name_lower or "rx 7" in name_lower)

        return gpus

    def _get_vendor_from_name(self, name: str) -> str:
        name_lower = name.lower()
        if "nvidia" in name_lower or "geforce" in name_lower:
            return "NVIDIA"
        if "amd" in name_lower or "radeon" in name_lower:
            return "AMD"
        if "intel" in name_lower:
            return "Intel"
        return "Unknown"

    def _detect_memory(self) -> Dict[str, Any]:
        """Detects system memory (RAM)."""
        if not psutil: return {}
        try:
            mem = psutil.virtual_memory()
            return {
                "total_mb": int(mem.total / (1024 * 1024)),
                "available_mb": int(mem.available / (1024 * 1024)),
            }
        except Exception as e:
            self.logger.error(f"Error detecting memory: {e}")
            return {}

    def _detect_os(self) -> Dict[str, str]:
        """Detects operating system information."""
        return {
            "name": platform.system(),
            "version": platform.version(),
            "release": platform.release(),
        }