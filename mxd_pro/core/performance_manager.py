import logging
from enum import Enum
from typing import Dict, Any
from .settings_engine import SettingsManager

class PerformanceMode(Enum):
    LOW_END = "Low-End"
    NORMAL = "Normal"
    HIGH_END = "High-End"

class PerformanceManager:
    """
    Determines hardware performance tier and manages feature availability.
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def determine_and_set_mode(self, hardware_info: Dict[str, Any], settings: SettingsManager) -> PerformanceMode:
        """
        Analyzes hardware and determines the appropriate performance mode.
        Saves the determined mode to settings.
        """
        cpu_cores = hardware_info.get("cpu", {}).get("cores", 0)
        ram_mb = hardware_info.get("memory", {}).get("total_mb", 0)

        mode = PerformanceMode.LOW_END # Default
        if cpu_cores >= 8 and ram_mb >= 12 * 1024:
            mode = PerformanceMode.HIGH_END
        elif cpu_cores >= 4 and ram_mb >= 6 * 1024:
            mode = PerformanceMode.NORMAL

        self.logger.info(f"Determined hardware performance mode: {mode.value}")
        settings.set_setting("app.performance_mode", mode.value)
        return mode

    def get_current_mode(self, settings: SettingsManager) -> PerformanceMode:
        """Retrieves the current performance mode from settings."""
        mode_str = settings.get_setting("app.performance_mode", PerformanceMode.LOW_END.value)
        try:
            return PerformanceMode(mode_str)
        except ValueError:
            return PerformanceMode.LOW_END

    def is_feature_unlocked(self, required_mode: PerformanceMode, current_mode: PerformanceMode) -> bool:
        """Checks if a feature is available for the current performance mode."""
        if current_mode == PerformanceMode.HIGH_END:
            return True
        if current_mode == PerformanceMode.NORMAL:
            return required_mode in [PerformanceMode.NORMAL, PerformanceMode.LOW_END]
        if current_mode == PerformanceMode.LOW_END:
            return required_mode == PerformanceMode.LOW_END
        return False