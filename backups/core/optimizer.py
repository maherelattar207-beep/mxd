import os
import sys
import json
import time
import copy
import threading
import subprocess
import configparser
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

import psutil
from PyQt5.QtCore import QObject, pyqtSignal
from .stability_monitor import StabilityMonitor

class OptimizationLevel(Enum): # ... (content unchanged)
    CONSERVATIVE = "conservative"; BALANCED = "balanced"; AGGRESSIVE = "aggressive"; ULTRA = "ultra"
class AIMode(Enum): # ... (content unchanged)
    BALANCED = "Balanced"; MAX_PERFORMANCE = "Max Performance"; MAX_QUALITY = "Max Quality"
class UpscalingTechnology(Enum): # ... (content unchanged)
    NONE = "none"; DLSS_QUALITY = "dlss_quality"; DLSS_BALANCED = "dlss_balanced"; DLSS_PERFORMANCE = "dlss_performance"; DLSS_ULTRA_PERFORMANCE = "dlss_ultra_performance"; FSR2_QUALITY = "fsr2_quality"; FSR2_BALANCED = "fsr2_balanced"; FSR2_PERFORMANCE = "fsr2_performance"; FSR2_ULTRA_QUALITY = "fsr2_ultra_quality"; FSR3_QUALITY = "fsr3_quality"; FSR3_BALANCED = "fsr3_balanced"; FSR3_PERFORMANCE = "fsr3_performance"; XESS_QUALITY = "xess_quality"; XESS_BALANCED = "xess_balanced"; XESS_PERFORMANCE = "xess_performance"; XESS_ULTRA_QUALITY = "xess_ultra_quality"

@dataclass
class GameProfile: # ... (content unchanged)
    name: str; executable_paths: List[str]; config_files: List[str]; resolution: str; target_fps: int; upscaling: UpscalingTechnology; frame_generation: bool; dynamic_resolution: bool; ray_tracing: bool; variable_rate_shading: bool; low_latency_mode: bool; optimization_level: OptimizationLevel; custom_settings: Dict[str, Any]; created_date: str; last_modified: str

class AIPerformanceOptimizer:
    def __init__(self, logger=None, settings=None):
        self.logger = logger
        self.settings = settings
    def _log(self, msg): self.logger.info(msg) if self.logger else None

    def analyze_system_performance(self, hardware_info: Dict[str, Any], mode: AIMode = AIMode.BALANCED) -> Dict[str, Any]:
        # ... (implementation unchanged)
        analysis = {"cpu_performance_class": "unknown", "gpu_performance_class": "unknown", "memory_adequacy": "unknown", "bottlenecks": [], "recommendations": []}
        try:
            cpu = hardware_info.get("cpu"); gpus = hardware_info.get("gpus", []); memory = hardware_info.get("memory")
            if cpu:
                if cpu.cores >= 8: analysis["cpu_performance_class"] = "high"
                elif cpu.cores >= 6: analysis["cpu_performance_class"] = "medium"
                else: analysis["cpu_performance_class"] = "low"
            if gpus and gpus[0].vram_mb >= 8192: analysis["gpu_performance_class"] = "high"
            elif gpus and gpus[0].vram_mb >= 6144: analysis["gpu_performance_class"] = "medium"
            else: analysis["gpu_performance_class"] = "low"
            if memory and memory.total_mb >= 16384: analysis["memory_adequacy"] = "good"
            else: analysis["memory_adequacy"] = "limited"
            self._generate_ai_recommendations(analysis, mode)
        except Exception as e: self._log(f"Error in AI analysis: {e}")
        return analysis

    def _generate_ai_recommendations(self, analysis: Dict[str, Any], mode: AIMode):
        # ... (implementation unchanged)
        recommendations = []; gpu_class = analysis["gpu_performance_class"]
        if mode == AIMode.MAX_PERFORMANCE: recommendations.extend(["Set Upscaling to: Performance", "Disable Ray Tracing"])
        elif mode == AIMode.MAX_QUALITY: recommendations.extend(["Set Upscaling to: Quality", "Enable Ray Tracing"])
        else: recommendations.append("Use Balanced settings for Upscaling and Ray Tracing.")
        analysis["recommendations"] = recommendations

    def _set_process_priority(self, exe_name: str, priority: str):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == exe_name:
                p = psutil.Process(proc.info['pid'])
                p.nice(psutil.HIGH_PRIORITY_CLASS if priority == "high" else psutil.NORMAL_PRIORITY_CLASS)
                self._log(f"Set priority for {exe_name} (PID: {p.pid}) to {priority}.")
                return True
        return False

    def _close_background_apps(self):
        apps_to_close = ["Spotify.exe", "Discord.exe", "steamwebhelper.exe", "msedgewebview2.exe"]
        closed_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] in apps_to_close:
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.terminate()
                    p.wait(timeout=3)
                    self._log(f"Closed background app: {proc.info['name']}")
                    closed_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
                    self._log(f"Could not close {proc.info['name']}: {e}")
        return closed_count

    def run_system_optimizations(self, game_profile: GameProfile, boost_priority: bool, close_apps: bool):
        self._log("Running advanced system optimizations...")
        if boost_priority:
            for exe in game_profile.executable_paths:
                if self._set_process_priority(exe, "high"): break
        if close_apps:
            self._close_background_apps()

class GamingOptimizer(QObject): # ... (rest of the class is unchanged)
    instability_reverted = pyqtSignal(str, str)
    def __init__(self, logger=None, settings=None):
        super().__init__();self.logger = logger;self.settings = settings
        self.profiles_file = Path("game_profiles.json")
        self.game_profiles = self._load_game_profiles()
        self.last_known_good_profiles = {}
        self.stability_monitor = StabilityMonitor(self.logger)
        self.stability_monitor.instability_detected.connect(self.revert_to_last_known_good)
    def _log(self, msg): self.logger.info(msg) if self.logger else None
    def _load_game_profiles(self):
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r', encoding='utf-8') as f: data = json.load(f)
                return {name: GameProfile(**pd) for name, pd in data.items()}
            except Exception as e: self._log(f"Error loading profiles: {e}")
        return self._create_default_profiles()
    def _save_game_profiles(self):
        try:
            with open(self.profiles_file, 'w', encoding='utf-8') as f: json.dump({name: asdict(p) for name, p in self.game_profiles.items()}, f, indent=2)
        except Exception as e: self._log(f"Error saving profiles: {e}")
    def _create_default_profiles(self):
        now = datetime.now().isoformat()
        return {"Cyberpunk 2077": GameProfile(name="Cyberpunk 2077", executable_paths=["Cyberpunk2077.exe"], config_files=["user.settings"], resolution="2560x1440", target_fps=60, upscaling=UpscalingTechnology.DLSS_BALANCED, frame_generation=True, dynamic_resolution=True, ray_tracing=True, variable_rate_shading=True, low_latency_mode=True, optimization_level=OptimizationLevel.BALANCED, custom_settings={}, created_date=now, last_modified=now)}
    def apply_game_optimization(self, game_name: str, hardware_info: Dict[str, Any]):
        if game_name not in self.game_profiles: return
        self.last_known_good_profiles[game_name] = copy.deepcopy(self.game_profiles[game_name])
        self.stability_monitor.start_monitoring(game_name)
    def revert_to_last_known_good(self, game_name: str):
        if game_name in self.last_known_good_profiles:
            self.game_profiles[game_name] = self.last_known_good_profiles[game_name]
            self._save_game_profiles()
            self.instability_reverted.emit(game_name, f"Reverted {game_name} settings to the last stable configuration.")
    def import_game_profiles(self, path): return True
    def export_game_profiles(self, path): return True
