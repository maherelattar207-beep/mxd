from enum import Enum

class PerformanceMode(Enum):
    LOW_END = "Low-End"
    NORMAL = "Normal"
    HIGH_END = "High-End"

class PerformanceManager:
    """
    Manages the application's performance mode based on system hardware.
    """
    def __init__(self, logger):
        self.logger = logger
        self.mode = PerformanceMode.NORMAL # Default mode

    def determine_and_set_mode(self, hardware_info, settings):
        """
        Determines the system's performance mode based on hardware and saves it to settings.
        This should only be run on the first launch.
        """
        if not settings.get("first_run", True):
            # If it's not the first run, load the existing mode from settings
            saved_mode = settings.get("performance_mode", PerformanceMode.NORMAL.value)
            self.mode = PerformanceMode(saved_mode)
            self.logger.info(f"Loaded performance mode from settings: {self.mode.value}")
            return self.mode

        self.logger.info("First run detected. Determining system performance mode...")

        try:
            cpu_cores = hardware_info.get("cpu").cores
            total_ram_gb = hardware_info.get("memory").total_mb / 1024
        except AttributeError:
            self.logger.warning("Could not retrieve full hardware info. Defaulting to Normal mode.")
            self.mode = PerformanceMode.NORMAL
            cpu_cores = 4
            total_ram_gb = 8

        self.logger.info(f"Detected System: {cpu_cores} CPU cores, {total_ram_gb:.2f} GB RAM")

        if total_ram_gb >= 8 and cpu_cores >= 4:
            self.mode = PerformanceMode.HIGH_END
        elif total_ram_gb <= 4 and cpu_cores <= 2:
            self.mode = PerformanceMode.LOW_END
        else: # Covers 6-8 GB RAM and 3-4 cores, and other edge cases
            self.mode = PerformanceMode.NORMAL

        self.logger.info(f"System performance mode set to: {self.mode.value}")

        # Save the determined mode to settings
        settings.set("performance_mode", self.mode.value)

        # We also set first_run to False now
        settings.set("first_run", False)

        return self.mode

    def get_mode(self):
        return self.mode

    def is_feature_unlocked(self, required_mode: PerformanceMode) -> bool:
        """
        Checks if a feature is unlocked based on the current performance mode.
        """
        if self.mode == PerformanceMode.HIGH_END:
            return True
        if self.mode == PerformanceMode.NORMAL:
            return required_mode != PerformanceMode.HIGH_END
        if self.mode == PerformanceMode.LOW_END:
            return required_mode == PerformanceMode.LOW_END

        return False
