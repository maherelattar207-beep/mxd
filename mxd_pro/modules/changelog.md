# MXD Pro - Changelog

All notable changes to this project will be documented in this file.

## [v2.0.0] - 2025-09-22

This is a massive overhaul of the MXD Pro application, moving from a simple optimizer to a feature-rich, AI-driven suite.

### Added
- **Core Architecture:** Refactored entire project into a modular `core`/`ui` structure.
- **AI-Powered Optimizer:**
    - New AI Modes: Balanced, Max Performance, and Max Quality.
    - "Auto-Optimize" button to apply AI-recommended settings directly to the UI.
    - AI-driven diagnostics and bottleneck detection on the System Info panel.
- **Advanced Game Optimizations:**
    - Full UI controls for FSR 2/3, DLSS 2/3, and XeSS quality modes.
    - Checkboxes for Frame Generation, NVIDIA Reflex, and Dynamic Resolution Scaling.
    - Advanced FPS boosting options: Set game process to high priority and close unnecessary background apps.
- **Response Time Optimization:**
    - New backend manager and UI controls for managing input latency (Safe, Balanced, Aggressive modes).
    - Simulated real-time latency display on the dashboard.
- **Stability & Rollback System:**
    - New background `StabilityMonitor` to detect (simulated) performance degradation.
    - System now automatically reverts to the last known good settings if instability is detected.
    - Users are notified via a popup dialog when a rollback occurs.
- **Hardware Monitoring:**
    - `HardwareDetector` significantly enhanced to provide real-time stats.
    - New System Info dashboard displays live data for CPU/GPU usage, clocks, temps, and VRAM usage.
- **Security & Privacy:**
    - Settings are now stored in an encrypted `settings.bin` file.
    - Logging is now directed to an encrypted file, written on application shutdown.
    - A "Clear User Data" button was added to the Settings panel to securely remove all logs, caches, and settings.
- **Licensing:**
    - The license system is now fully automatic. It generates a valid license on first run without user interaction. The license dialog has been removed.
- **Performance Profiles:**
    - The application now automatically detects system hardware on first run and assigns a Low-End, Normal, or High-End performance profile, which gates access to certain high-impact features.
- **Multi-Language Support:**
    - Added a `LocalizationManager` and placeholder JSON files for 16 languages.
    - Language can be changed in the Settings panel.
- **UI Overhaul:**
    - Implemented a new professional Red/Gold/Black theme via QSS.
    - All UI panels have been rebuilt with a clean, modern, and organized layout.
- **Reporting:**
    - A "First-Time Setup" summary report is shown to the user on first launch.

### Changed
- Rewrote `optimizer_panel.py` from scratch to be a fully functional UI.
- Rewrote `sysinfo_panel.py` to be a dynamic, real-time dashboard.
- Replaced old `hardware.py` and `optimizer.py` logic with new, more powerful versions.
- `main.py` updated to initialize and integrate all new backend managers.

### Removed
- Removed the old, non-functional UI panels.
- Removed the manual license activation dialog (`license_dialog.py`).
