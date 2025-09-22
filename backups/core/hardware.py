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
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

# Try to import platform-specific modules
try:
    import psutil
except ImportError:
    psutil = None

try:
    if platform.system() == "Windows":
        import wmi
    else:
        wmi = None
except ImportError:
    wmi = None

@dataclass
class GPUInfo:
    """GPU information structure"""
    name: str = "N/A"
    vendor: str = "N/A"
    vram_mb: int = 0
    driver_version: str = "N/A"
    pci_id: str = "N/A"
    # Capabilities
    supports_6k: bool = False
    supports_rt: bool = False
    supports_dlss: bool = False
    supports_fsr: bool = True # Assume modern GPUs can try FSR
    supports_xess: bool = False
    # Real-time stats
    utilization: float = 0.0
    vram_usage_percent: float = 0.0
    temperature: float = 0.0
    core_clock_mhz: float = 0.0
    mem_clock_mhz: float = 0.0
    power_draw_w: float = 0.0

@dataclass
class CPUInfo:
    """CPU information structure"""
    name: str = "N/A"
    vendor: str = "N/A"
    cores: int = 0
    threads: int = 0
    base_frequency: float = 0.0
    max_frequency: float = 0.0
    # Real-time stats
    current_frequency: float = 0.0
    utilization: float = 0.0
    per_core_utilization: List[float] = field(default_factory=list)
    temperature: float = 0.0 # Not reliably available via psutil on all platforms

@dataclass
class MemoryInfo:
    """Memory information structure"""
    total_mb: int = 0
    available_mb: int = 0
    used_mb: int = 0
    usage_percent: float = 0.0

class HardwareDetector:
    """Accurate hardware detection with real information only"""

    def __init__(self, logger=None):
        self.logger = logger
        self._gpu_cache = None
        self._cpu_cache = None
        self._log("Hardware detector initialized")

    def _log(self, message: str, level: str = "info"):
        if self.logger:
            getattr(self.logger, level, self.logger.info)(message)

    def get_system_summary(self) -> Dict[str, any]:
        """Get complete system hardware summary. Caches results."""
        if self._cpu_cache and self._gpu_cache:
            return {
                "cpu": self._cpu_cache,
                "gpus": self._gpu_cache,
                "memory": self.detect_memory(),
            }

        self._cpu_cache = self.detect_cpu()
        self._gpu_cache = self.detect_gpus()

        summary = {
            "cpu": self._cpu_cache,
            "gpus": self._gpu_cache,
            "memory": self.detect_memory(),
        }
        self._log("Generated complete system hardware summary")
        return summary

    def get_realtime_stats(self) -> Dict[str, Any]:
        """Fetches only the real-time, volatile hardware stats."""
        cpu_stats = {"utilization": 0.0, "per_core_utilization": [], "current_frequency": 0.0}
        gpu_stats = {"utilization": 0.0, "vram_usage_percent": 0.0, "temperature": 0.0, "core_clock_mhz": 0.0, "mem_clock_mhz": 0.0, "power_draw_w": 0.0}

        # CPU Stats
        if psutil:
            cpu_stats["utilization"] = psutil.cpu_percent(interval=None)
            cpu_stats["per_core_utilization"] = psutil.cpu_percent(interval=None, percpu=True)
            try:
                cpu_stats["current_frequency"] = psutil.cpu_freq().current
            except Exception:
                pass # Some systems block this

        # GPU Stats (currently NVIDIA-only via nvidia-smi)
        if self._gpu_cache and self._gpu_cache[0].vendor == "NVIDIA":
            gpu_stats = self._get_nvidia_smi_stats()

        return {"cpu": cpu_stats, "gpu": gpu_stats}

    def _get_nvidia_smi_stats(self) -> Dict[str, Any]:
        """Helper to get real-time stats from nvidia-smi."""
        stats = {"utilization": 0.0, "vram_usage_percent": 0.0, "temperature": 0.0, "core_clock_mhz": 0.0, "mem_clock_mhz": 0.0, "power_draw_w": 0.0}
        try:
            # Using XML output is more robust than CSV parsing
            result = subprocess.run(
                ['nvidia-smi', '-q', '-x'],
                capture_output=True, text=True, check=True
            )
            root = ET.fromstring(result.stdout)
            gpu = root.find('gpu')
            if not gpu:
                return stats

            # Safely extract values
            def find_and_get_text(path, unit_multiplier=1.0):
                elem = gpu.find(path)
                if elem is not None and elem.text and "N/A" not in elem.text:
                    return float(re.sub(r'[^0-9.]', '', elem.text)) * unit_multiplier
                return 0.0

            stats["utilization"] = find_and_get_text('utilization/gpu_util')
            stats["temperature"] = find_and_get_text('temperature/gpu_temp')
            stats["power_draw_w"] = find_and_get_text('power_readings/power_draw')
            stats["core_clock_mhz"] = find_and_get_text('clocks/graphics_clock')
            stats["mem_clock_mhz"] = find_and_get_text('clocks/mem_clock')

            total_mem = find_and_get_text('fb_memory_usage/total', 1024*1024)
            used_mem = find_and_get_text('fb_memory_usage/used', 1024*1024)
            stats["vram_usage_percent"] = (used_mem / total_mem) * 100 if total_mem > 0 else 0.0

        except (FileNotFoundError, subprocess.CalledProcessError, ET.ParseError) as e:
            self._log(f"Could not get nvidia-smi stats: {e}", level="warning")
        except Exception as e:
            self._log(f"An unexpected error occurred while fetching nvidia-smi stats: {e}", level="error")

        return stats

    def detect_gpus(self) -> List[GPUInfo]:
        """Detect GPUs with accurate information."""
        if self._gpu_cache:
            return self._gpu_cache

        gpus = []
        try:
            if platform.system() == "Windows" and wmi:
                c = wmi.WMI()
                video_controllers = c.Win32_VideoController()
                if video_controllers:
                    gpu_data = video_controllers[0]
                    gpu = GPUInfo(
                        name=gpu_data.Name.strip(),
                        vram_mb=int(gpu_data.AdapterRAM / (1024*1024)) if gpu_data.AdapterRAM else 0,
                        driver_version=gpu_data.DriverVersion or "N/A",
                        pci_id=gpu_data.PNPDeviceID or "N/A"
                    )
                    if "nvidia" in gpu.name.lower(): gpu.vendor = "NVIDIA"
                    elif "amd" in gpu.name.lower(): gpu.vendor = "AMD"
                    elif "intel" in gpu.name.lower(): gpu.vendor = "Intel"

                    gpu.supports_dlss = gpu.vendor == "NVIDIA" and "rtx" in gpu.name.lower()
                    gpu.supports_xess = gpu.vendor == "Intel" and "arc" in gpu.name.lower()
                    gpu.supports_rt = ("rtx" in gpu.name.lower() or "rx 6" in gpu.name.lower() or "rx 7" in gpu.name.lower() or "arc" in gpu.name.lower())
                    gpu.supports_6k = gpu.vram_mb >= 8192

                    if gpu.vendor == "NVIDIA":
                        realtime_stats = self._get_nvidia_smi_stats()
                        for key, value in realtime_stats.items():
                            setattr(gpu, key, value)

                    gpus.append(gpu)
        except Exception as e:
            self._log(f"WMI GPU detection failed: {e}", level="error")

        if not gpus:
            self._log("No GPUs detected via primary methods. Using fallback.", level="warning")
            gpus.append(GPUInfo()) # Append default N/A object

        self._gpu_cache = gpus
        return gpus

    def detect_cpu(self) -> CPUInfo:
        """Detect CPU information."""
        if self._cpu_cache:
            return self._cpu_cache

        cpu = CPUInfo()
        if not psutil:
            self._log("psutil not found, cannot detect CPU info.", level="error")
            return cpu

        try:
            cpu.name = platform.processor() or "N/A"
            if "intel" in cpu.name.lower(): cpu.vendor = "Intel"
            elif "amd" in cpu.name.lower(): cpu.vendor = "AMD"

            cpu.cores = psutil.cpu_count(logical=False) or 0
            cpu.threads = psutil.cpu_count(logical=True) or 0

            freq = psutil.cpu_freq()
            cpu.current_frequency = freq.current
            cpu.max_frequency = freq.max
            cpu.base_frequency = freq.min

            cpu.utilization = psutil.cpu_percent(interval=1)
            cpu.per_core_utilization = psutil.cpu_percent(interval=None, percpu=True)

        except Exception as e:
            self._log(f"Error detecting CPU: {e}", level="error")

        self._cpu_cache = cpu
        return cpu

    def detect_memory(self) -> MemoryInfo:
        """Detect system memory information."""
        mem_info = MemoryInfo()
        if not psutil:
            self._log("psutil not found, cannot detect memory info.", level="error")
            return mem_info
        try:
            mem = psutil.virtual_memory()
            mem_info.total_mb = int(mem.total / (1024 * 1024))
            mem_info.available_mb = int(mem.available / (1024 * 1024))
            mem_info.used_mb = int(mem.used / (1024 * 1024))
            mem_info.usage_percent = mem.percent
        except Exception as e:
            self._log(f"Error detecting memory: {e}", level="error")
        return mem_info
