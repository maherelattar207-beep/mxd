import random
from enum import Enum

class ResponseMode(Enum):
    SAFE = "Safe"
    BALANCED = "Balanced"
    AGGRESSIVE = "Aggressive"

class ResponseTimeManager:
    """
    Manages response time and input latency optimizations.
    NOTE: The actual latency reduction is simulated. This class provides the
    framework for a real implementation.
    """
    def __init__(self, logger, settings):
        self.logger = logger
        self.settings = settings
        self.current_mode = ResponseMode.SAFE
        self.base_latency_ms = 15.0 # A typical baseline for a good system

    def set_mode(self, mode: ResponseMode):
        """Sets the desired latency reduction mode."""
        self.current_mode = mode
        self.settings.set("response_time.mode", mode.value)
        self.logger.info(f"Response Time Optimization mode set to: {mode.value}")
        self.apply_latency_tweaks()

    def apply_latency_tweaks(self):
        """
        Applies the tweaks associated with the current mode.
        This is a placeholder for real system changes.
        """
        if self.current_mode == ResponseMode.SAFE:
            self.logger.info("Applying SAFE latency tweaks (e.g., standard low latency modes).")
        elif self.current_mode == ResponseMode.BALANCED:
            self.logger.info("Applying BALANCED latency tweaks (e.g., Reflex + Boost).")
        elif self.current_mode == ResponseMode.AGGRESSIVE:
            self.logger.info("Applying AGGRESSIVE latency tweaks (e.g., overriding pre-rendered frames).")

        # In a real app, this would modify driver settings, config files, etc.

    def get_simulated_latency(self) -> float:
        """
        Returns a simulated latency value in ms based on the current mode.
        """
        if self.current_mode == ResponseMode.SAFE:
            # Small, stable reduction
            return self.base_latency_ms - random.uniform(1, 3)
        elif self.current_mode == ResponseMode.BALANCED:
            # Good reduction with slight variance
            return self.base_latency_ms - random.uniform(3, 6)
        elif self.current_mode == ResponseMode.AGGRESSIVE:
            # Max reduction with more variance
            return self.base_latency_ms - random.uniform(6, 10)

        return self.base_latency_ms
