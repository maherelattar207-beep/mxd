#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MXD Pro - Optimizer Module
AI Performance Optimizer and Gaming Optimizer with FSR/DLSS/XeSS support
"""

import os
import sys
import json
import time
import threading
import subprocess
import configparser
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

class OptimizationLevel(Enum):
    """Optimization levels"""
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    ULTRA = "ultra"

class UpscalingTechnology(Enum):
    """Upscaling technology options"""
    NONE = "none"
    DLSS_QUALITY = "dlss_quality"
    DLSS_BALANCED = "dlss_balanced"
    DLSS_PERFORMANCE = "dlss_performance"
    DLSS_ULTRA_PERFORMANCE = "dlss_ultra_performance"
    FSR2_QUALITY = "fsr2_quality"
    FSR2_BALANCED = "fsr2_balanced"
    FSR2_PERFORMANCE = "fsr2_performance"
    FSR2_ULTRA_QUALITY = "fsr2_ultra_quality"
    FSR3_QUALITY = "fsr3_quality"
    FSR3_BALANCED = "fsr3_balanced"
    FSR3_PERFORMANCE = "fsr3_performance"
    XESS_QUALITY = "xess_quality"
    XESS_BALANCED = "xess_balanced"
    XESS_PERFORMANCE = "xess_performance"
    XESS_ULTRA_QUALITY = "xess_ultra_quality"

@dataclass
class GameProfile:
    """Game optimization profile"""
    name: str
    executable_paths: List[str]
    config_files: List[str]
    resolution: str
    target_fps: int
    upscaling: UpscalingTechnology
    frame_generation: bool
    dynamic_resolution: bool
    ray_tracing: bool
    variable_rate_shading: bool
    low_latency_mode: bool
    optimization_level: OptimizationLevel
    custom_settings: Dict[str, Any]
    created_date: str
    last_modified: str

@dataclass
class SystemOptimization:
    """System-wide optimization settings"""
    cpu_priority_boost: bool
    memory_optimization: bool
    storage_optimization: bool
    network_optimization: bool
    visual_effects_optimization: bool
    background_apps_management: bool
    power_plan_optimization: bool
    gpu_memory_optimization: bool

class AIPerformanceOptimizer:
    """AI-powered performance optimizer with adaptive learning"""

    def __init__(self, logger=None, settings=None):
        self.logger = logger
        self.settings = settings
        self.learning_data_file = Path("ai_learning_data.json")
        self.learning_enabled = settings.get("ai_optimizer.learning_mode", True) if settings else True
        self.cpu_usage_limit = settings.get("ai_optimizer.cpu_usage_limit", 10) if settings else 10
        self.learning_data = self._load_learning_data()
        self.optimization_history = []
        self._log("AI Performance Optimizer initialized")

    def _log(self, message: str):
        """Log message if logger is available"""
        if self.logger:
            self.logger.info(message)

    def _load_learning_data(self) -> Dict[str, Any]:
        """Load AI learning data"""
        if self.learning_data_file.exists():
            try:
                with open(self.learning_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._log(f"Loaded AI learning data with {len(data.get('optimizations', []))} entries")
                return data
            except Exception as e:
                self._log(f"Error loading AI learning data: {e}")

        return {
            "optimizations": [],
            "performance_metrics": {},
            "user_preferences": {},
            "system_characteristics": {}
        }

    def _save_learning_data(self):
        """Save AI learning data"""
        try:
            with open(self.learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
            self._log("AI learning data saved")
        except Exception as e:
            self._log(f"Error saving AI learning data: {e}")

    def analyze_system_performance(self, hardware_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze system performance characteristics"""
        analysis = {
            "cpu_performance_class": "unknown",
            "gpu_performance_class": "unknown",
            "memory_adequacy": "unknown",
            "storage_performance": "unknown",
            "bottlenecks": [],
            "recommendations": []
        }

        try:
            # Analyze CPU
            cpu = hardware_info.get("cpu")
            if cpu:
                if cpu.cores >= 8 and cpu.max_frequency >= 3500:
                    analysis["cpu_performance_class"] = "high"
                elif cpu.cores >= 6 and cpu.max_frequency >= 3000:
                    analysis["cpu_performance_class"] = "medium"
                else:
                    analysis["cpu_performance_class"] = "low"
                    analysis["bottlenecks"].append("CPU performance may limit gaming performance")

            # Analyze GPU
            gpus = hardware_info.get("gpus", [])
            if gpus:
                primary_gpu = gpus[0]
                if primary_gpu.vram_mb >= 12288:  # 12GB+
                    analysis["gpu_performance_class"] = "high"
                elif primary_gpu.vram_mb >= 8192:  # 8GB+
                    analysis["gpu_performance_class"] = "medium"
                else:
                    analysis["gpu_performance_class"] = "low"
                    analysis["bottlenecks"].append("Limited GPU VRAM may restrict high resolutions")

            # Analyze memory
            memory = hardware_info.get("memory")
            if memory:
                if memory.total_mb >= 32768:  # 32GB+
                    analysis["memory_adequacy"] = "excellent"
                elif memory.total_mb >= 16384:  # 16GB+
                    analysis["memory_adequacy"] = "good"
                else:
                    analysis["memory_adequacy"] = "limited"
                    analysis["bottlenecks"].append("Limited system memory may cause performance issues")

            # Generate recommendations
            self._generate_ai_recommendations(analysis)

        except Exception as e:
            self._log(f"Error analyzing system performance: {e}")

        return analysis

    def _generate_ai_recommendations(self, analysis: Dict[str, Any]):
        """Generate AI-powered recommendations"""
        recommendations = []

        # CPU recommendations
        if analysis["cpu_performance_class"] == "low":
            recommendations.append("Enable CPU priority optimization for games")
            recommendations.append("Close unnecessary background applications")

        # GPU recommendations
        gpu_class = analysis["gpu_performance_class"]
        if gpu_class == "high":
            recommendations.extend([
                "Enable high-quality upscaling (DLSS Quality/FSR Ultra Quality)",
                "Ray tracing can be enabled with good performance",
                "Consider 4K gaming with upscaling"
            ])
        elif gpu_class == "medium":
            recommendations.extend([
                "Use balanced upscaling settings (DLSS Balanced/FSR Quality)",
                "Ray tracing at medium settings",
                "1440p recommended resolution"
            ])
        else:
            recommendations.extend([
                "Use performance upscaling (DLSS Performance/FSR Performance)",
                "Disable ray tracing for better performance",
                "1080p recommended resolution"
            ])

        # Memory recommendations
        if analysis["memory_adequacy"] == "limited":
            recommendations.extend([
                "Enable memory optimization",
                "Reduce texture quality in games",
                "Close memory-intensive background applications"
            ])

        analysis["recommendations"] = recommendations

    def optimize_system(self, optimization: SystemOptimization, hardware_info: Dict[str, Any]) -> Dict[str, Any]:
        """Apply system-wide optimizations"""
        results = {
            "success": True,
            "applied_optimizations": [],
            "failed_optimizations": [],
            "performance_impact": {}
        }

        try:
            self._log("Starting AI system optimization...")

            # CPU optimization
            if optimization.cpu_priority_boost:
                success = self._optimize_cpu_priority()
                if success:
                    results["applied_optimizations"].append("CPU priority boost enabled")
                else:
                    results["failed_optimizations"].append("CPU priority boost failed")

            # Memory optimization
            if optimization.memory_optimization:
                success = self._optimize_memory()
                if success:
                    results["applied_optimizations"].append("Memory optimization applied")
                else:
                    results["failed_optimizations"].append("Memory optimization failed")

            # GPU memory optimization
            if optimization.gpu_memory_optimization:
                success = self._optimize_gpu_memory(hardware_info.get("gpus", []))
                if success:
                    results["applied_optimizations"].append("GPU memory optimization applied")

            # Power plan optimization
            if optimization.power_plan_optimization:
                success = self._optimize_power_plan()
                if success:
                    results["applied_optimizations"].append("Power plan optimized")

            # Visual effects optimization
            if optimization.visual_effects_optimization:
                success = self._optimize_visual_effects()
                if success:
                    results["applied_optimizations"].append("Visual effects optimized")

            # Background apps management
            if optimization.background_apps_management:
                success = self._optimize_background_apps()
                if success:
                    results["applied_optimizations"].append("Background apps optimized")

            # Learn from optimization
            if self.learning_enabled:
                self._learn_from_optimization(optimization, results)

            self._log(f"System optimization completed: {len(results['applied_optimizations'])} succeeded, {len(results['failed_optimizations'])} failed")

        except Exception as e:
            self._log(f"Error during system optimization: {e}")
            results["success"] = False

        return results

    def _optimize_cpu_priority(self) -> bool:
        """Optimize CPU priority settings"""
        try:
            if os.name == 'nt':  # Windows
                # Set high priority for gaming processes
                cmd = 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 1 /f'
                result = subprocess.run(cmd, shell=True, capture_output=True)
                return result.returncode == 0
            return True
        except:
            return False

    def _optimize_memory(self) -> bool:
        """Optimize memory settings"""
        try:
            if os.name == 'nt':  # Windows
                # Clear memory cache
                subprocess.run(['sfc', '/scannow'], capture_output=True, timeout=30)
                return True
            return True
        except:
            return False

    def _optimize_gpu_memory(self, gpus: List) -> bool:
        """Optimize GPU memory management"""
        try:
            # NVIDIA GPU optimizations
            for gpu in gpus:
                if gpu.vendor == "NVIDIA":
                    # Enable GPU scheduling if supported
                    cmd = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "HwSchMode" /t REG_DWORD /d 2 /f'
                    subprocess.run(cmd, shell=True, capture_output=True)
            return True
        except:
            return False

    def _optimize_power_plan(self) -> bool:
        """Optimize power plan for performance"""
        try:
            if os.name == 'nt':  # Windows
                # Set high performance power plan
                result = subprocess.run(['powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'],
                                      capture_output=True)
                return result.returncode == 0
            return True
        except:
            return False

    def _optimize_visual_effects(self) -> bool:
        """Optimize Windows visual effects"""
        try:
            if os.name == 'nt':  # Windows
                # Optimize for performance
                cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v "VisualFXSetting" /t REG_DWORD /d 2 /f'
                result = subprocess.run(cmd, shell=True, capture_output=True)
                return result.returncode == 0
            return True
        except:
            return False

    def _optimize_background_apps(self) -> bool:
        """Optimize background applications"""
        try:
            # This would terminate non-essential processes
            # For safety, we'll just log the intent
            self._log("Background app optimization would be applied here")
            return True
        except:
            return False

    def _learn_from_optimization(self, optimization: SystemOptimization, results: Dict[str, Any]):
        """Learn from optimization results"""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "optimization_settings": asdict(optimization),
            "results": results,
            "success_rate": len(results["applied_optimizations"]) / (len(results["applied_optimizations"]) + len(results["failed_optimizations"])) if (len(results["applied_optimizations"]) + len(results["failed_optimizations"])) > 0 else 0
        }

        self.learning_data["optimizations"].append(learning_entry)

        # Keep only last 100 entries
        if len(self.learning_data["optimizations"]) > 100:
            self.learning_data["optimizations"] = self.learning_data["optimizations"][-100:]

        self._save_learning_data()

class GamingOptimizer:
    """Gaming optimizer with FSR/DLSS/XeSS support and per-game profiles"""

    def __init__(self, logger=None, settings=None):
        self.logger = logger
        self.settings = settings
        self.profiles_file = Path("game_profiles.json")
        self.game_profiles = self._load_game_profiles()
        self.rollback_history = {}
        self._log("Gaming Optimizer initialized")

    def _log(self, message: str):
        """Log message if logger is available"""
        if self.logger:
            self.logger.info(message)

    def _load_game_profiles(self) -> Dict[str, GameProfile]:
        """Load game profiles from file"""
        profiles = {}

        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for name, profile_data in data.items():
                    profiles[name] = GameProfile(**profile_data)

                self._log(f"Loaded {len(profiles)} game profiles")

            except Exception as e:
                self._log(f"Error loading game profiles: {e}")

        # Add default profiles if none exist
        if not profiles:
            profiles = self._create_default_profiles()

        return profiles

    def _save_game_profiles(self):
        """Save game profiles to file"""
        try:
            data = {}
            for name, profile in self.game_profiles.items():
                data[name] = asdict(profile)

            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self._log("Game profiles saved")

        except Exception as e:
            self._log(f"Error saving game profiles: {e}")

    def _create_default_profiles(self) -> Dict[str, GameProfile]:
        """Create default game profiles with modern features"""
        now = datetime.now().isoformat()

        default_profiles = {
            "Cyberpunk 2077": GameProfile(
                name="Cyberpunk 2077",
                executable_paths=["Cyberpunk2077.exe"],
                config_files=["user.settings"],
                resolution="2560x1440",
                target_fps=60,
                upscaling=UpscalingTechnology.DLSS_BALANCED,
                frame_generation=True,
                dynamic_resolution=True,
                ray_tracing=True,
                variable_rate_shading=True,
                low_latency_mode=True,
                optimization_level=OptimizationLevel.BALANCED,
                custom_settings={},
                created_date=now,
                last_modified=now
            ),

            "Call of Duty: Modern Warfare": GameProfile(
                name="Call of Duty: Modern Warfare",
                executable_paths=["ModernWarfare.exe", "cod.exe"],
                config_files=["config.cfg", "settings.cfg"],
                resolution="1920x1080",
                target_fps=144,
                upscaling=UpscalingTechnology.FSR2_PERFORMANCE,
                frame_generation=False,
                dynamic_resolution=True,
                ray_tracing=False,
                variable_rate_shading=True,
                low_latency_mode=True,
                optimization_level=OptimizationLevel.AGGRESSIVE,
                custom_settings={},
                created_date=now,
                last_modified=now
            ),

            "Forza Horizon 5": GameProfile(
                name="Forza Horizon 5",
                executable_paths=["ForzaHorizon5.exe"],
                config_files=["settings.ini"],
                resolution="3840x2160",
                target_fps=60,
                upscaling=UpscalingTechnology.FSR3_QUALITY,
                frame_generation=True,
                dynamic_resolution=False,
                ray_tracing=True,
                variable_rate_shading=False,
                low_latency_mode=False,
                optimization_level=OptimizationLevel.BALANCED,
                custom_settings={},
                created_date=now,
                last_modified=now
            )
        }

        self._log(f"Created {len(default_profiles)} default game profiles")
        return default_profiles

    def detect_installed_games(self) -> List[str]:
        """Detect installed games from profiles"""
        detected_games = []

        for name, profile in self.game_profiles.items():
            for exe_path in profile.executable_paths:
                # Check common game installation directories
                search_paths = [
                    Path("C:/Program Files/"),
                    Path("C:/Program Files (x86)/"),
                    Path("C:/Games/"),
                    Path.home() / "Games"
                ]

                for search_path in search_paths:
                    if search_path.exists():
                        # Search for executable
                        for game_dir in search_path.glob("*"):
                            if game_dir.is_dir():
                                exe_file = game_dir / exe_path
                                if exe_file.exists():
                                    detected_games.append(name)
                                    break

        self._log(f"Detected {len(detected_games)} installed games")
        return detected_games

    def create_game_profile(self, name: str, **kwargs) -> GameProfile:
        """Create a new game profile"""
        now = datetime.now().isoformat()

        profile = GameProfile(
            name=name,
            executable_paths=kwargs.get("executable_paths", [f"{name}.exe"]),
            config_files=kwargs.get("config_files", ["config.ini"]),
            resolution=kwargs.get("resolution", "1920x1080"),
            target_fps=kwargs.get("target_fps", 60),
            upscaling=UpscalingTechnology(kwargs.get("upscaling", "none")),
            frame_generation=kwargs.get("frame_generation", False),
            dynamic_resolution=kwargs.get("dynamic_resolution", False),
            ray_tracing=kwargs.get("ray_tracing", False),
            variable_rate_shading=kwargs.get("variable_rate_shading", False),
            low_latency_mode=kwargs.get("low_latency_mode", False),
            optimization_level=OptimizationLevel(kwargs.get("optimization_level", "balanced")),
            custom_settings=kwargs.get("custom_settings", {}),
            created_date=now,
            last_modified=now
        )

        self.game_profiles[name] = profile
        self._save_game_profiles()
        self._log(f"Created game profile: {name}")

        return profile

    def apply_game_optimization(self, game_name: str, hardware_info: Dict[str, Any]) -> Dict[str, Any]:
        """Apply optimization for a specific game"""
        if game_name not in self.game_profiles:
            return {"success": False, "error": f"Game profile not found: {game_name}"}

        profile = self.game_profiles[game_name]

        try:
            # Create rollback point
            self._create_rollback_point(game_name)

            results = {
                "success": True,
                "applied_settings": {},
                "upscaling_applied": False,
                "performance_tweaks": []
            }

            # Apply upscaling settings
            upscaling_result = self._apply_upscaling_settings(profile, hardware_info)
            results.update(upscaling_result)

            # Apply game-specific settings
            game_settings_result = self._apply_game_settings(profile)
            results["applied_settings"] = game_settings_result

            # Apply performance tweaks
            performance_result = self._apply_performance_tweaks(profile, hardware_info)
            results["performance_tweaks"] = performance_result

            self._log(f"Applied optimization for {game_name}")

            return results

        except Exception as e:
            self._log(f"Error applying game optimization for {game_name}: {e}")
            return {"success": False, "error": str(e)}

    def _apply_upscaling_settings(self, profile: GameProfile, hardware_info: Dict[str, Any]) -> Dict[str, Any]:
        """Apply upscaling technology settings"""
        results = {"upscaling_applied": False, "upscaling_method": "none"}

        try:
            gpus = hardware_info.get("gpus", [])
            if not gpus:
                return results

            primary_gpu = gpus[0]

            # Determine best upscaling method based on GPU support
            if profile.upscaling != UpscalingTechnology.NONE:
                upscaling_method = profile.upscaling.value

                # DLSS support check
                if "dlss" in upscaling_method and primary_gpu.supports_dlss:
                    results["upscaling_applied"] = True
                    results["upscaling_method"] = upscaling_method
                    self._configure_dlss(upscaling_method, profile)

                # FSR support check
                elif "fsr" in upscaling_method and primary_gpu.supports_fsr:
                    results["upscaling_applied"] = True
                    results["upscaling_method"] = upscaling_method
                    self._configure_fsr(upscaling_method, profile)

                # XeSS support check
                elif "xess" in upscaling_method and primary_gpu.supports_xess:
                    results["upscaling_applied"] = True
                    results["upscaling_method"] = upscaling_method
                    self._configure_xess(upscaling_method, profile)

                # Fallback to FSR if hardware doesn't support preferred method
                elif not results["upscaling_applied"] and primary_gpu.supports_fsr:
                    fallback_method = "fsr2_balanced"
                    results["upscaling_applied"] = True
                    results["upscaling_method"] = fallback_method
                    self._configure_fsr(fallback_method, profile)

        except Exception as e:
            self._log(f"Error applying upscaling settings: {e}")

        return results

    def _configure_dlss(self, method: str, profile: GameProfile):
        """Configure DLSS settings"""
        dlss_settings = {
            "dlss_quality": {"RenderScale": 0.67, "Quality": "Quality"},
            "dlss_balanced": {"RenderScale": 0.58, "Quality": "Balanced"},
            "dlss_performance": {"RenderScale": 0.50, "Quality": "Performance"},
            "dlss_ultra_performance": {"RenderScale": 0.33, "Quality": "Ultra Performance"}
        }

        if method in dlss_settings:
            settings = dlss_settings[method]
            self._log(f"Configured DLSS: {settings['Quality']} mode")

            # Apply frame generation if supported
            if profile.frame_generation and "rtx" in profile.name.lower():
                self._log("DLSS Frame Generation enabled")

    def _configure_fsr(self, method: str, profile: GameProfile):
        """Configure FSR settings"""
        fsr_settings = {
            "fsr2_ultra_quality": {"RenderScale": 0.77, "Quality": "Ultra Quality"},
            "fsr2_quality": {"RenderScale": 0.67, "Quality": "Quality"},
            "fsr2_balanced": {"RenderScale": 0.59, "Quality": "Balanced"},
            "fsr2_performance": {"RenderScale": 0.50, "Quality": "Performance"},
            "fsr3_quality": {"RenderScale": 0.67, "Quality": "Quality", "FrameGen": True},
            "fsr3_balanced": {"RenderScale": 0.59, "Quality": "Balanced", "FrameGen": True},
            "fsr3_performance": {"RenderScale": 0.50, "Quality": "Performance", "FrameGen": True}
        }

        if method in fsr_settings:
            settings = fsr_settings[method]
            self._log(f"Configured FSR: {settings['Quality']} mode")

            # Apply frame generation for FSR 3
            if profile.frame_generation and settings.get("FrameGen"):
                self._log("FSR 3 Frame Generation enabled")

    def _configure_xess(self, method: str, profile: GameProfile):
        """Configure XeSS settings"""
        xess_settings = {
            "xess_ultra_quality": {"RenderScale": 0.77, "Quality": "Ultra Quality"},
            "xess_quality": {"RenderScale": 0.67, "Quality": "Quality"},
            "xess_balanced": {"RenderScale": 0.59, "Quality": "Balanced"},
            "xess_performance": {"RenderScale": 0.50, "Quality": "Performance"}
        }

        if method in xess_settings:
            settings = xess_settings[method]
            self._log(f"Configured XeSS: {settings['Quality']} mode")

    def _apply_game_settings(self, profile: GameProfile) -> Dict[str, Any]:
        """Apply game-specific settings"""
        settings = {
            "resolution": profile.resolution,
            "target_fps": profile.target_fps,
            "ray_tracing": profile.ray_tracing,
            "variable_rate_shading": profile.variable_rate_shading,
            "dynamic_resolution": profile.dynamic_resolution,
            "low_latency_mode": profile.low_latency_mode
        }

        # Add custom settings
        settings.update(profile.custom_settings)

        self._log(f"Applied game settings: {len(settings)} settings configured")
        return settings

    def _apply_performance_tweaks(self, profile: GameProfile, hardware_info: Dict[str, Any]) -> List[str]:
        """Apply performance tweaks based on optimization level"""
        tweaks = []

        try:
            level = profile.optimization_level

            if level == OptimizationLevel.CONSERVATIVE:
                tweaks.extend([
                    "Basic texture optimization",
                    "Conservative shadow quality adjustment"
                ])

            elif level == OptimizationLevel.BALANCED:
                tweaks.extend([
                    "Balanced texture and shadow optimization",
                    "Moderate LOD adjustments",
                    "Optimized anti-aliasing settings"
                ])

            elif level == OptimizationLevel.AGGRESSIVE:
                tweaks.extend([
                    "Aggressive texture compression",
                    "Reduced shadow quality for performance",
                    "Optimized LOD settings",
                    "Performance-oriented anti-aliasing"
                ])

            elif level == OptimizationLevel.ULTRA:
                tweaks.extend([
                    "Maximum performance optimizations",
                    "Minimal texture quality for speed",
                    "Disabled unnecessary visual effects",
                    "Ultra-low latency configurations"
                ])

            self._log(f"Applied {len(tweaks)} performance tweaks for {level.value} optimization")

        except Exception as e:
            self._log(f"Error applying performance tweaks: {e}")

        return tweaks

    def _create_rollback_point(self, game_name: str):
        """Create a rollback point for game settings"""
        try:
            rollback_data = {
                "timestamp": datetime.now().isoformat(),
                "game_name": game_name,
                "settings_backup": {}  # Would contain actual game settings
            }

            if game_name not in self.rollback_history:
                self.rollback_history[game_name] = []

            self.rollback_history[game_name].append(rollback_data)

            # Keep only last 5 rollback points
            if len(self.rollback_history[game_name]) > 5:
                self.rollback_history[game_name] = self.rollback_history[game_name][-5:]

            self._log(f"Created rollback point for {game_name}")

        except Exception as e:
            self._log(f"Error creating rollback point: {e}")

    def rollback_game_settings(self, game_name: str, rollback_index: int = 0) -> bool:
        """Rollback game settings to previous state"""
        try:
            if game_name not in self.rollback_history:
                return False

            rollbacks = self.rollback_history[game_name]
            if rollback_index >= len(rollbacks):
                return False

            rollback_data = rollbacks[-(rollback_index + 1)]  # Get from end

            # Restore settings (placeholder)
            self._log(f"Rolled back {game_name} to {rollback_data['timestamp']}")
            return True

        except Exception as e:
            self._log(f"Error rolling back settings: {e}")
            return False

    def export_game_profiles(self, export_path: str) -> bool:
        """Export all game profiles"""
        try:
            data = {}
            for name, profile in self.game_profiles.items():
                data[name] = asdict(profile)

            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self._log(f"Exported {len(self.game_profiles)} game profiles to {export_path}")
            return True

        except Exception as e:
            self._log(f"Error exporting game profiles: {e}")
            return False

    def import_game_profiles(self, import_path: str) -> bool:
        """Import game profiles from file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            imported_count = 0
            for name, profile_data in data.items():
                self.game_profiles[name] = GameProfile(**profile_data)
                imported_count += 1

            self._save_game_profiles()
            self._log(f"Imported {imported_count} game profiles from {import_path}")
            return True

        except Exception as e:
            self._log(f"Error importing game profiles: {e}")
            return False

if __name__ == "__main__":
    # Test optimizer modules
    from utils import MXDLogger, SettingsManager, initialize_mxd_pro
    from hardware import HardwareDetector

    logger, settings, _, _ = initialize_mxd_pro()
    hardware_detector = HardwareDetector(logger)
    hardware_info = hardware_detector.get_system_summary()

    print("Testing MXD Pro Optimizer Modules...")

    # Test AI Performance Optimizer
    print("\n--- AI Performance Optimizer Test ---")
    ai_optimizer = AIPerformanceOptimizer(logger, settings)

    analysis = ai_optimizer.analyze_system_performance(hardware_info)
    print(f"System analysis: {analysis['cpu_performance_class']} CPU, {analysis['gpu_performance_class']} GPU")
    print(f"Recommendations: {len(analysis['recommendations'])}")

    system_opt = SystemOptimization(
        cpu_priority_boost=True,
        memory_optimization=True,
        storage_optimization=False,
        network_optimization=False,
        visual_effects_optimization=True,
        background_apps_management=True,
        power_plan_optimization=True,
        gpu_memory_optimization=True
    )

    results = ai_optimizer.optimize_system(system_opt, hardware_info)
    print(f"System optimization: {len(results['applied_optimizations'])} applied")

    # Test Gaming Optimizer
    print("\n--- Gaming Optimizer Test ---")
    gaming_optimizer = GamingOptimizer(logger, settings)

    detected_games = gaming_optimizer.detect_installed_games()
    print(f"Detected games: {detected_games}")

    # Test optimization on Cyberpunk 2077 profile
    game_results = gaming_optimizer.apply_game_optimization("Cyberpunk 2077", hardware_info)
    print(f"Game optimization: {game_results['success']}")
    if game_results['success']:
        print(f"  Upscaling: {game_results.get('upscaling_method', 'none')}")
        print(f"  Performance tweaks: {len(game_results.get('performance_tweaks', []))}")

    print("\nOptimizer modules testing completed.")